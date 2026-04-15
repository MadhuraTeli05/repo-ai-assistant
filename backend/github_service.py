"""
GitHub Repository Integration

This module handles all interactions with the GitHub API:
- Fetching file listings from repositories
- Downloading file contents
- Handling rate limiting and errors gracefully
"""

import requests
import time
import logging
from config import (
    GITHUB_TOKEN,
    SKIP_FOLDERS,
    MAX_GITHUB_DEPTH,
    GITHUB_REQUEST_TIMEOUT,
    GITHUB_REQUEST_DELAY,
)

logger = logging.getLogger(__name__)

# GitHub API requires authentication in request headers
# This token acts like a password and increases rate limits from 60 to 6000 requests/hour
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def fetch_repo_files(owner: str, repo: str, path: str = "", depth: int = 0) -> list:
    """
    Fetch all files from a GitHub repository recursively.
    
    This function:
    - Fetches file/folder listings from GitHub API
    - Recursively explores directories (with depth limit)
    - Filters out unwanted folders (docs, tests, etc.)
    - Includes delay to avoid rate limiting
    
    Args:
        owner (str): Repository owner (e.g., "fastapi")
        repo (str): Repository name (e.g., "fastapi")
        path (str): Path within repo to fetch from (empty = root)
        depth (int): Current recursion depth (to prevent infinite loops)
        
    Returns:
        list: List of file objects with keys: type, name, path, download_url
        
    Example:
        >>> files = fetch_repo_files("fastapi", "fastapi")
        >>> print(f"Found {len(files)} files")
        >>> fastapi_files = [f for f in files if f["name"].endswith(".py")]
        >>> print(f"Python files: {len(fastapi_files)}")
    """
    
    # ✅ Depth limit prevents infinite folder traversal
    # GitHub repos can have very deep nested folders
    if depth > MAX_GITHUB_DEPTH:
        logger.debug(f"Max depth ({MAX_GITHUB_DEPTH}) reached, stopping recursion")
        return []
    
    # Construct GitHub API URL for this path
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    try:
        logger.debug(f"Fetching from: {url}")
        
        # Make API request with timeout
        response = requests.get(url, headers=headers, timeout=GITHUB_REQUEST_TIMEOUT)
        
        # Check if request succeeded
        if response.status_code == 404:
            logger.error(f"Repository not found: {owner}/{repo}")
            return []
        elif response.status_code == 403:
            logger.error("GitHub API rate limited! Check GITHUB_TOKEN.")
            return []
        elif response.status_code != 200:
            logger.warning(f"GitHub API returned {response.status_code} at {url}")
            return []
        
        # Parse JSON response
        items = response.json()
        all_files = []
        
        # Process each item (file or folder)
        for item in items:
            try:
                # ✅ If it's a file → collect it
                if item["type"] == "file":
                    all_files.append(item)
                    logger.debug(f"  Found file: {item['name']}")
                
                # ✅ If it's a directory → explore it (recursively)
                elif item["type"] == "dir":
                    # Skip unwanted folders to save time and API calls
                    if any(skip in item["path"] for skip in SKIP_FOLDERS):
                        logger.debug(f"  Skipped folder: {item['path']} (in skip list)")
                        continue
                    
                    logger.debug(f"  Exploring folder: {item['path']}")
                    
                    # Recursively fetch from subdirectory
                    subfolder_files = fetch_repo_files(
                        owner, repo, item["path"], depth + 1
                    )
                    all_files.extend(subfolder_files)
                
                # Add delay to prevent overwhelming the API
                time.sleep(GITHUB_REQUEST_DELAY)
            
            except Exception as e:
                logger.warning(f"Error processing item {item.get('name', 'unknown')}: {e}")
                continue
        
        logger.info(f"Fetched {len(all_files)} files from {'root' if not path else path}")
        return all_files
    
    except requests.exceptions.Timeout:
        logger.error(f"Request timeout while fetching {url}")
        return []
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error while fetching {url}")
        return []
    except Exception as e:
        logger.error(f"Failed to fetch repository files: {e}")
        return []


def fetch_file_content(download_url: str) -> str:
    """
    Download raw file content from GitHub.
    
    GitHub provides a raw.githubusercontent.com URL for downloading
    the actual file content instead of the API JSON response.
    
    Args:
        download_url (str): GitHub API download_url field (points to raw file)
        
    Returns:
        str: File contents as string, or None if download failed
        
    Example:
        >>> code = fetch_file_content("https://raw.githubusercontent.com/...")
        >>> if code:
        ...     print(f"Downloaded {len(code)} bytes")
        ... else:
        ...     print("Download failed")
    """
    
    if not download_url:
        logger.warning("download_url is empty")
        return None
    
    try:
        logger.debug(f"Downloading: {download_url}")
        
        # Download file content
        response = requests.get(
            download_url,
            timeout=GITHUB_REQUEST_TIMEOUT,
            headers=headers
        )
        
        if response.status_code == 200:
            logger.debug(f"Successfully downloaded {len(response.text)} bytes")
            return response.text
        else:
            logger.warning(f"Failed to download: HTTP {response.status_code}")
            return None
    
    except requests.exceptions.Timeout:
        logger.warning(f"Timeout downloading file: {download_url}")
        return None
    except requests.exceptions.ConnectionError:
        logger.warning(f"Connection error downloading file: {download_url}")
        return None
    except Exception as e:
        logger.error(f"Error downloading file {download_url}: {e}")
        return None
