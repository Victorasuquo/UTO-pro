# import os
# import requests
# from dotenv import load_dotenv
# from langchain_core.documents import Document

# load_dotenv()

# github_token = os.getenv("GITHUB_TOKEN")


# def fetch_github(owner, repo, endpoint):
#     url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
#     headers = {"Authorization": f"Bearer {github_token}"}
#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         data = response.json()
#     else:
#         print("Failed with status code:", response.status_code)
#         return []

#     print(data)
#     return data


# def fetch_github_issues(owner, repo):
#     data = fetch_github(owner, repo, "issues")
#     return load_issues(data)


# def load_issues(issues):
#     docs = []
#     for entry in issues:
#         metadata = {
#             "author": entry["user"]["login"],
#             "comments": entry["comments"],
#             "body": entry["body"],
#             "labels": entry["labels"],
#             "created_at": entry["created_at"],
#         }
#         data = entry["title"]
#         if entry["body"]:
#             data += entry["body"]
#         doc = Document(page_content=data, metadata=metadata)
#         docs.append(doc)

#     return docs

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
        data = response.json()
    else:
        print("Failed with status code:", response.status_code)
        return []

    print(data)
    return data


def fetch_github_issues(owner, repo):
    return fetch_github(owner, repo, "issues")


def fetch_github_repositories(query, max_results=5):
    url = "https://api.github.com/search/repositories"
    headers = {"Authorization": f"Bearer {github_token}"}
    params = {"q": query, "per_page": max_results}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        repositories = data["items"]  # Extracting items from search results
    else:
        print("Failed with status code:", response.status_code)
        repositories = []

    return repositories


def load_issues(issues):
    docs = []
    for entry in issues:
        metadata = {
            "author": entry["user"]["login"],
            "comments": entry["comments"],
            "body": entry["body"],
            "labels": entry["labels"],
            "created_at": entry["created_at"],
        }
        data = entry["title"]
        if entry["body"]:
            data += entry["body"]
        doc = Document(page_content=data, metadata=metadata)
        docs.append(doc)

    return docs
