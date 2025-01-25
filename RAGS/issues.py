# from dotenv import load_dotenv
# import os

# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_astradb import AstraDBVectorStore
# from langchain.agents import create_tool_calling_agent
# from langchain.agents import AgentExecutor
# from langchain.tools.retriever import create_retriever_tool
# from langchain import hub
# from github import fetch_github_issues
# from note import note_tool

# load_dotenv()


# def connect_to_vstore():
#     embeddings = OpenAIEmbeddings()
#     ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
#     ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
#     desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")

#     if desired_namespace:
#         ASTRA_DB_KEYSPACE = desired_namespace
#     else:
#         ASTRA_DB_KEYSPACE = None

#     vstore = AstraDBVectorStore(
#         embedding=embeddings,
#         collection_name="github",
#         api_endpoint=ASTRA_DB_API_ENDPOINT,
#         token=ASTRA_DB_APPLICATION_TOKEN,
#         namespace=ASTRA_DB_KEYSPACE,
#     )
#     return vstore


# vstore = connect_to_vstore()
# add_to_vectorstore = input("Do you want to update the issues? (y/N): ").lower() in [
#     "yes",
#     "y",
# ]

# if add_to_vectorstore:
#     owner = "google"
#     repo = "it-cert-automation-practice"
#     issues = fetch_github_issues(owner, repo)

#     try:
#         vstore.delete_collection()
#     except:
#         pass

#     vstore = connect_to_vstore()
#     vstore.add_documents(issues)

#     # results = vstore.similarity_search("flash messages", k=3)
#     # for res in results:
#     #     print(f"* {res.page_content} {res.metadata}")

# retriever = vstore.as_retriever(search_kwargs={"k": 3})
# retriever_tool = create_retriever_tool(
#     retriever,
#     "github_search",
#     "Search for information about github issues. For any questions about github issues, you must use this tool!",
# )

# prompt = hub.pull("hwchase17/openai-functions-agent")
# llm = ChatOpenAI()

# tools = [retriever_tool, note_tool]
# agent = create_tool_calling_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# while (question := input("Ask a question about github issues (q to quit): ")) != "q":
#     result = agent_executor.invoke({"input": question})
#     print(result["output"])

from dotenv import load_dotenv
import os
import requests
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from github import fetch_github_issues, fetch_github_repositories, load_issues

load_dotenv()

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

vstore = connect_to_vstore()

def update_issues(owner, repo):
    issues = fetch_github_issues(owner, repo)

    try:
        vstore.delete_collection()
    except:
        pass

    vstore = connect_to_vstore()
    vstore.add_documents(issues)

retriever = vstore.as_retriever(search_kwargs={"k": 3})
retriever_tool = create_retriever_tool(
    retriever,
    "github_search",
    "Search for information about github issues. For any questions about github issues, you must use this tool!",
)

prompt = hub.pull("hwchase17/openai-functions-agent")
llm = ChatOpenAI()

tools = [retriever_tool]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

while True:
    action = input("Do you want to search for repositories (r) or ask about issues (i)? (q to quit): ").lower()
    if action == "q":
        break
    elif action == "r":
        query = input("Enter keywords to search GitHub repositories: ")
        repositories = fetch_github_repositories(query, max_results=5)
        print("Top 5 repositories matching your query:")
        for index, repo in enumerate(repositories, start=1):
            print(f"{index}. {repo['full_name']}")
        repo_index = int(input("Select a repository (1-5): ")) - 1
        if 0 <= repo_index < len(repositories):
            selected_repo = repositories[repo_index]
            owner, repo_name = selected_repo['owner']['login'], selected_repo['name']
            update_issues(owner, repo_name)
            print(f"Issues updated for repository {owner}/{repo_name}")
        else:
            print("Invalid selection")
    elif action == "i":
        question = input("Ask a question about github issues (q to quit): ")
        if question == "q":
            break
        result = agent_executor.invoke({"input": question})
        print(result["output"])
    else:
        print("Invalid action")
