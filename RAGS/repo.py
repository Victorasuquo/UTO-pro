import os
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

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

def analyze_repositories(query, context, max_results=7):
    repositories = fetch_github_repositories(query, max_results=max_results)
    matched_repos = []

    for repo in repositories:
        owner, repo_name = repo["owner"]["login"], repo["name"]
        readme_content = fetch_readme(owner, repo_name)

        if context.lower() in readme_content.lower():
            matched_repos.append({
                "name": repo_name,
                "owner": owner,
                "url": repo["html_url"],
                "description": repo.get("description", "No description"),
                "readme_snippet": readme_content[:500],  # Include a snippet of the README
            })

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
            print(f"   README Snippet: {repo['readme_snippet']}")
            print("---")

# Example usage
if __name__ == "__main__":
    search_query = input("Enter keywords to search repositories: ")
    context = input("Enter the context to match in README files: ")

    matched_repositories = analyze_repositories(search_query, context)
    display_matched_repositories(matched_repositories)
