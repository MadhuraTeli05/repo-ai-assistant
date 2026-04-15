# RAG Application - Setup & Installation Guide

## Project Overview

This is a **Retrieval-Augmented Generation (RAG)** system for semantic code search.
It allows you to search GitHub repositories using natural language questions instead of keywords.

### Key Features:
- ✅ Fetch code from GitHub repositories
- ✅ Extract functions and classes using AST
- ✅ Generate semantic embeddings
- ✅ Store embeddings in vector database (ChromaDB)
- ✅ Search semantically (find similar code by meaning)
- ✅ REST API for integration with other services
- ✅ Interactive CLI for testing

---

## Quick Start (5 steps)

### Step 1: Get GitHub Token
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Select scope: `public_repo`
4. Copy the token (you'll need it in Step 3)

### Step 2: Create .env file
In `backend/backend/` folder, create `.env`:

```bash
# Copy from .env.example
cp .env.example .env

# Edit .env and replace:
# GITHUB_TOKEN=ghp_your_token_here
```

Or manually create `.env` with:
```
GITHUB_TOKEN=ghp_your_token_here
```

### Step 3: Install Dependencies
```bash
# Navigate to project directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1

# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Step 4: Run the Application
```bash
# Navigate to folder with main.py
cd backend

# Option 1: Interactive mode (build DB + search)
python main.py

# Option 2: Build database only
python main.py --build

# Option 3: Search only
python main.py --search "your question"

# Option 4: Show statistics
python main.py --stats

# Option 5: Force rebuild
python main.py --rebuild
```

### Step 5: Use the REST API (Optional)
```bash
# Start API server
uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Then visit:
# - Interactive docs: http://localhost:8000/docs
# - Search: POST /search
# - Build DB: POST /build
# - Stats: GET /stats
```

---

## File Structure

```
backend/backend/
├── main.py                  # CLI entry point
├── api.py                   # FastAPI REST endpoints
├── config.py                # Configuration management
├── rag_pipeline.py          # Core RAG orchestration
├── github_service.py        # GitHub API integration
├── parser.py                # Code parsing (AST)
├── embeddings.py            # Text → vectors
├── vector_store.py          # Vector DB (ChromaDB)
├── chunking.py              # Code chunking strategies
├── requirements.txt         # Python dependencies
├── .env.example             # Sample configuration
└── .env                     # Your actual secrets (in .gitignore)
```

---

## How It Works

```
GitHub Repo
    ↓
[github_service.py] → Fetch Python files
    ↓
[parser.py] → Extract functions & classes
    ↓
[chunking.py] → Split large chunks
    ↓
[embeddings.py] → Convert to vectors (384 numbers)
    ↓
[vector_store.py] → Store in ChromaDB
    ↓
[rag_pipeline.py] → Orchestrates above
    ↓
Search: Convert question → vector → find similar
    ↓
Return relevant code chunks to user
```

---

## Example Usage

### Interactive Mode
```bash
$ python main.py

🚀 RAG APPLICATION - Interactive Mode

📦 STEP 1: Initializing Database
   Repository: fastapi/fastapi

[Building database... may take 10-30 minutes]

📊 STEP 2: Database Statistics
Total entries: 1250
...

📊 STEP 3: Ask Questions

❓ Ask a question: How to handle errors?

✅ Found 5 relevant code chunks:

#1 - error_handler (function)
   File: fastapi/exception_handlers.py
   🎯 Relevance: 95%
   💻 Code:
   def error_handler(request, exc):
       """Handle exceptions and return JSON"""
       ...

[Show results for #2, #3, #4, #5]
```

### CLI Mode
```bash
# Search only
python main.py --search "How to parse JSON?"

# Build only
python main.py --build

# Statistics
python main.py --stats
```

### REST API
```bash
# Start API
uvicorn api:app --reload

# Search via curl
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "How to handle errors?", "n_results": 5}'

# Response:
{
  "query": "How to handle errors?",
  "total_matches": 2,
  "matches": [
    {
      "rank": 1,
      "name": "error_handler",
      "type": "function",
      "file": "framework.py",
      "similarity": 0.95,
      "code": "def error_handler(...)..."
    }
  ]
}
```

---

## Configuration

All settings are in `.env`. Key settings:

| Setting | Default | Description |
|---------|---------|-------------|
| `GITHUB_TOKEN` | - | GitHub API token (required) |
| `GITHUB_OWNER` | fastapi | GitHub repo owner |
| `GITHUB_REPO` | fastapi | GitHub repo name |
| `CHROMA_DB_PATH` | chroma_db | Vector DB location |
| `EMBEDDINGS_MODEL` | all-MiniLM-L6-v2 | Embedding model |
| `SEARCH_RESULTS_COUNT` | 5 | Default results |
| `API_PORT` | 8000 | API server port |
| `LOG_LEVEL` | INFO | Logging level |

See `.env.example` for all options.

---

## Troubleshooting

### ❌ GITHUB_TOKEN not found
**Error:** `ValueError: GITHUB_TOKEN not found in .env file!`

**Solution:** Create/edit `.env` file:
```
GITHUB_TOKEN=ghp_your_token_here
```

### ❌ GitHub API 403 Error
**Error:** `GitHub API rate limited`

**Solution:** 
- Check your GITHUB_TOKEN is correct
- Wait 1 hour for rate limit reset
- Use `GITHUB_REQUEST_DELAY` to slow down requests

### ❌ Module not found errors
**Error:** `ModuleNotFoundError: No module named 'chromadb'`

**Solution:** Install dependencies:
```bash
pip install -r backend/requirements.txt
```

### ❌ Slow first run
**Note:** First build takes 10-30 minutes for large repos. This is normal!

Subsequent runs use cached `chroma_db/` folder and are instant.

### ❌ Out of memory
**Error:** Building stops with memory error

**Solution:**
- Reduce `MAX_GITHUB_DEPTH` in `.env`
- Use smaller repository
- Increase available RAM

---

## Performance Tips

1. **First run is slow**: Database building downloads and processes files (10-30 min for FastAPI)
2. **Subsequent searches are instant**: Uses cached embeddings
3. **Search quality**: Better with more relevant queries
4. **Memory**: Each embedding = ~1.5KB, 1000 chunks = ~1.5MB

---

## API Documentation

Visit **http://localhost:8000/docs** (after starting API) for:
- ✅ Interactive testing
- ✅ Request/response examples
- ✅ Parameter documentation
- ✅ Try it out functionality

---

## Extending the Project

### Add a New Repository
```python
from rag_pipeline import get_pipeline

pipeline = get_pipeline()
pipeline.build_database(owner="django", repo="django")
pipeline.search("How to use Django signals?")
```

### Use Custom Embeddings Model
Update `.env`:
```
EMBEDDINGS_MODEL=all-mpnet-base-v2
```

### Integrate with Your App
```python
from rag_pipeline import get_pipeline

pipeline = get_pipeline()
results = pipeline.search("your question")

for match in results['matches']:
    print(f"{match['name']}: {match['similarity']}% relevant")
```

---

## Next Steps

1. ✅ Complete the setup above
2. ✅ Run with `python main.py`
3. ✅ Try searching for code
4. ✅ (Optional) Start API with `uvicorn api:app --reload`
5. ✅ (Optional) Customize settings in `.env`

---

## Support

For issues:
1. Check `.env` has `GITHUB_TOKEN`
2. Read error messages carefully
3. Check logs in terminal
4. See Troubleshooting section above

Good luck! 🚀
