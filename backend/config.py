"""
Configuration Management for RAG Application

This module loads and manages all configuration settings from environment variables.
It provides default values and validates required settings.
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# GitHub Configuration
# ============================================================================

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("❌ GITHUB_TOKEN not found in .env file! Please add it.")

# Default GitHub repository to process
DEFAULT_GITHUB_OWNER = os.getenv("GITHUB_OWNER", "fastapi")
DEFAULT_GITHUB_REPO = os.getenv("GITHUB_REPO", "fastapi")

# Maximum recursion depth when fetching GitHub repo (prevents infinite loops)
MAX_GITHUB_DEPTH = int(os.getenv("MAX_GITHUB_DEPTH", "2"))

# Folders to skip during GitHub traversal (reduce unnecessary downloads)
SKIP_FOLDERS = ["docs", "tests", ".github", "images", "examples", "build", "dist"]

# Request timeout for GitHub API calls (seconds)
GITHUB_REQUEST_TIMEOUT = int(os.getenv("GITHUB_REQUEST_TIMEOUT", "30"))

# Delay between GitHub API requests (avoid rate limiting)
GITHUB_REQUEST_DELAY = float(os.getenv("GITHUB_REQUEST_DELAY", "0.2"))

# ============================================================================
# Vector Database Configuration (ChromaDB)
# ============================================================================

# Path where ChromaDB stores embeddings and metadata
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "chroma_db")

# Collection name in ChromaDB (like a table in SQL)
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "repo_chunks")

# ============================================================================
# Embeddings Configuration
# ============================================================================

# Model used to convert text to embeddings
# "all-MiniLM-L6-v2" - lightweight, fast, good for semantic search
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")

# Dimension of embedding vectors (384 for MiniLM model)
EMBEDDINGS_DIMENSION = int(os.getenv("EMBEDDINGS_DIMENSION", "384"))

# ============================================================================
# Search Configuration
# ============================================================================

# Number of search results to return by default
SEARCH_RESULTS_COUNT = int(os.getenv("SEARCH_RESULTS_COUNT", "5"))

# Similarity threshold (0-1, higher = more strict matching)
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.0"))

# ============================================================================
# FastAPI Configuration
# ============================================================================

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_RELOAD = os.getenv("API_RELOAD", "True").lower() == "true"

# ============================================================================
# Code Processing Configuration
# ============================================================================

# Supported file extensions to process
SUPPORTED_EXTENSIONS = [".py"]

# Maximum file size to process (in bytes, default 1MB)
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "1048576"))

# Chunk size for code splitting (lines)
CHUNK_SIZE_LINES = int(os.getenv("CHUNK_SIZE_LINES", "50"))

# Overlap between chunks (lines, for context preservation)
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "10"))

# ============================================================================
# Logging Configuration
# ============================================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logger.setLevel(LOG_LEVEL)

# ============================================================================
# Validation & Logging
# ============================================================================

logger.info(f"✅ Configuration loaded successfully")
logger.info(f"   GitHub Repo: {DEFAULT_GITHUB_OWNER}/{DEFAULT_GITHUB_REPO}")
logger.info(f"   ChromaDB Path: {CHROMA_DB_PATH}")
logger.info(f"   Embeddings Model: {EMBEDDINGS_MODEL}")
logger.info(f"   API: http://{API_HOST}:{API_PORT}")
