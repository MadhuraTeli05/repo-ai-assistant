import requests
import time

# 🔑 Replace with your GitHub token from env file ...GitHub API needs authentication ..Token acts like password ..Headers send that token with every request..Without this → you got 403 error earlier..👉 Now → you get 200 OK
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

#Get all files from a GitHub repo with controlled depth and filtering. This function is recursive, meaning it calls itself to explore directories within the repository. It also includes a delay between requests to avoid overwhelming the GitHub API.
def fetch_repo_files(owner, repo, path="", depth=0):
    """
    Recursively fetch repository files with controlled depth and filtering
    """

    # ✅ Limit recursion depth (VERY IMPORTANT) ..Stops infinite folder traversal..Prevents crash/network overload
    if depth > 2:
        return []

    #gihub api call to get files and folders 
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    try:
        response = requests.get(url, headers=headers)   #header contains the authentication token required to access the GitHub API

        if response.status_code != 200:                   #Handles API failure safely..If the API call fails (e.g., due to network issues or rate limits), it logs the error and returns an empty list instead of crashing the program.
            print(f"Error {response.status_code} at {url}")
            return []

        items = response.json()             #Converts API response into Python data 
        all_files = []

        for item in items:

            # ✅ If it's a file → store it
            if item["type"] == "file":
                all_files.append(item)

            # ✅ If it's a directory → go deeper (but filter unwanted folders)
            elif item["type"] == "dir":

                # ❌ Skip heavy/unnecessary folders
                if any(skip in item["path"] for skip in ["docs", "tests", ".github", "images"]):
                    continue

                all_files.extend(
                    fetch_repo_files(owner, repo, item["path"], depth + 1)     #Goes inside folder ..Calls itself again..recursion call
                )

            # ✅ Add small delay to prevent network crash
            time.sleep(0.2)

        return all_files

    except Exception as e:
        print("Request failed:", e)
        return []


def fetch_file_content(download_url):
    """
    Fetch raw file content from GitHub
    """

    if not download_url:
        return None

    try:
        response = requests.get(download_url)

        if response.status_code == 200:
            return response.text

    except Exception as e:
        print("Error fetching file:", e)

    return None