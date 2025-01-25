import os
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain import hub
from concurrent.futures import ThreadPoolExecutor
from sentence_transformers import SentenceTransformer, util

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

# Initialize a sentence transformer model for semantic similarity
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

def fetch_github(owner, repo, endpoint):
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
    headers = {"Authorization": f"Bearer {github_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch {endpoint} with status code: {response.status_code}")
        return None

def fetch_github_repositories(query, max_results=7):
    url = "https://api.github.com/search/repositories"
    headers = {"Authorization": f"Bearer {github_token}"}
    params = {"q": query, "per_page": max_results}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data["items"]  # Extract repositories
    else:
        print(f"Failed to search repositories with status code: {response.status_code}")
        return []

def fetch_readme(owner, repo):
    readme_data = fetch_github(owner, repo, "readme")
    if readme_data and "content" in readme_data:
        import base64
        content = base64.b64decode(readme_data["content"]).decode("utf-8")
        return content
    else:
        print(f"No README found for {owner}/{repo}")
        return ""

def analyze_repository(repo, context_embedding):
    owner, repo_name = repo["owner"]["login"], repo["name"]
    readme_content = fetch_readme(owner, repo_name)

    if readme_content:
        readme_embedding = semantic_model.encode(readme_content, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(context_embedding, readme_embedding).item()

        if similarity > 0.75:  # Threshold for semantic similarity
            return {
                "name": repo_name,
                "owner": owner,
                "url": repo["html_url"],
                "description": repo.get("description", "No description"),
                "readme_snippet": readme_content[:500],  # Include a snippet of the README
                "similarity": similarity,
            }
    return None

def analyze_repositories(query, context, max_results=7):
    repositories = fetch_github_repositories(query, max_results=max_results)
    context_embedding = semantic_model.encode(context, convert_to_tensor=True)
    matched_repos = []

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda repo: analyze_repository(repo, context_embedding), repositories))

    for result in results:
        if result:
            matched_repos.append(result)

    matched_repos.sort(key=lambda x: x["similarity"], reverse=True)
    return matched_repos

def display_matched_repositories(matched_repos):
    if not matched_repos:
        print("No repositories matched the given context.")
    else:
        print("Matched Repositories:")
        for idx, repo in enumerate(matched_repos, start=1):
            print(f"{idx}. {repo['name']} ({repo['owner']})")
            print(f"   URL: {repo['url']}")
            print(f"   Description: {repo['description']}")
            print(f"   Similarity: {repo['similarity']:.2f}")
            print(f"   README Snippet: {repo['readme_snippet']}")
            print("---")

def connect_to_vstore():
    embeddings = OpenAIEmbeddings()
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")

    if desired_namespace:
        ASTRA_DB_KEYSPACE = desired_namespace
    else:
        ASTRA_DB_KEYSPACE = None

    vstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="github",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )
    return vstore

if __name__ == "__main__":
    search_query = input("Enter keywords to search repositories: ")
    context = input("Enter the context to match in README files: ")

    matched_repositories = analyze_repositories(search_query, context)
    display_matched_repositories(matched_repositories)

    # Connect to vector store for RAG functionality
    vstore = connect_to_vstore()

    add_to_vectorstore = input("Do you want to update the RAG with matched repositories? (y/N): ").lower() in ["yes", "y"]

    if add_to_vectorstore:
        documents = []
        for repo in matched_repositories:
            document = Document(
                page_content=repo["readme_snippet"],
                metadata={"name": repo["name"], "url": repo["url"], "description": repo["description"]},
            )
            documents.append(document)

        try:
            vstore.delete_collection()
        except:
            pass

        vstore.add_documents(documents)

    retriever = vstore.as_retriever(search_kwargs={"k": 3})
    retriever_tool = create_retriever_tool(
        retriever,
        "repository_search",
        "Search for information in matched repositories' README files.",
    )

    prompt = hub.pull("hwchase17/openai-functions-agent")
    llm = ChatOpenAI()

    tools = [retriever_tool]
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    while (question := input("Ask a question about matched repositories (q to quit): ")) != "q":
        result = agent_executor.invoke({"input": question})
        print(result["output"])
