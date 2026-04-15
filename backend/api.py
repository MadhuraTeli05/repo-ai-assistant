"""
FastAPI REST API Endpoints for RAG Application

This module provides REST API endpoints for the RAG system,
allowing web and mobile clients to interact with the system.

Launch the API with:
    uvicorn api:app --reload --host 0.0.0.0 --port 8000

Then visit: http://localhost:8000/docs (interactive API documentation)
"""

import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_pipeline import get_pipeline
from vector_store import get_db_stats
from config import API_HOST, API_PORT

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG API",
    description="Retrieval-Augmented Generation API for semantic code search",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Request/Response Models
# ============================================================================

class SearchQuery(BaseModel):
    """Request model for search endpoint."""
    query: str
    n_results: int = 5


class CodeMatch(BaseModel):
    """Code chunk match from search results."""
    rank: int
    name: str
    type: str  # "function" or "class"
    file: str
    similarity: Optional[float] = None
    code: str


class SearchResponse(BaseModel):
    """Response model for search endpoint."""
    query: str
    total_matches: int
    matches: List[CodeMatch]


class BuildDatabaseRequest(BaseModel):
    """Request model for database build."""
    owner: str = "fastapi"
    repo: str = "fastapi"
    force_rebuild: bool = False


class DatabaseStats(BaseModel):
    """Database statistics model."""
    total_chunks: int
    unique_files: int
    files: List[str]


class BuildStatus(BaseModel):
    """Status of database build operation."""
    success: bool
    message: str
    stats: Optional[dict] = None


# ============================================================================
# Helper Functions
# ============================================================================

def format_code_preview(code: str, max_length: int = 500) -> str:
    """Format code for API response (limit length)."""
    if len(code) <= max_length:
        return code
    return code[:max_length] + f"\n... ({len(code) - max_length} more characters)"


# ============================================================================
# Health & Info Endpoints
# ============================================================================

@app.get("/", tags=["Health"])
def root():
    """Root endpoint with API info."""
    return {
        "name": "RAG API",
        "description": "Retrieval-Augmented Generation for semantic code search",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "✅ OK"}


# ============================================================================
# Search Endpoints
# ============================================================================

@app.post("/search", response_model=SearchResponse, tags=["Search"])
def search(request: SearchQuery):
    """
    Search for relevant code chunks using semantic similarity.
    
    **Parameters:**
    - `query` (str): Natural language question about code
    - `n_results` (int): Number of results to return (default: 5)
    
    **Returns:**
    - List of matching code chunks with relevance scores
    
    **Example:**
    ```json
    {
      "query": "How to handle errors?",
      "total_matches": 2,
      "matches": [
        {
          "rank": 1,
          "name": "error_handler",
          "type": "function",
          "file": "utils.py",
          "similarity": 0.95,
          "code": "def error_handler(...)..."
        }
      ]
    }
    ```
    """
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        pipeline = get_pipeline()
        results = pipeline.search(request.query, n_results=request.n_results)
        
        # Format matches
        formatted_matches = []
        for match in results.get('matches', []):
            formatted_matches.append(CodeMatch(
                rank=match['rank'],
                name=match['name'],
                type=match['type'],
                file=match['file'],
                similarity=match.get('similarity'),
                code=format_code_preview(match['code'])
            ))
        
        return SearchResponse(
            query=request.query,
            total_matches=len(formatted_matches),
            matches=formatted_matches
        )
    
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search", tags=["Search"])
def search_get(
    q: str = Query(..., min_length=1, description="Search query"),
    n_results: int = Query(5, ge=1, le=50, description="Number of results")
):
    """
    Simple search endpoint (GET method).
    
    **URL Parameters:**
    - `q`: Query string (required)
    - `n_results`: Number of results (default: 5, max: 50)
    
    **Example:** `/search?q=error+handling&n_results=3`
    """
    request = SearchQuery(query=q, n_results=n_results)
    return search(request)


# ============================================================================
# Database Management Endpoints
# ============================================================================

@app.post("/build", response_model=BuildStatus, tags=["Database"])
def build_database(request: BuildDatabaseRequest):
    """
    Build/rebuild embeddings database from GitHub repository.
    
    **Parameters:**
    - `owner` (str): GitHub repository owner (default: "fastapi")
    - `repo` (str): GitHub repository name (default: "fastapi")
    - `force_rebuild` (bool): Clear existing data and rebuild (default: false)
    
    **Warning:** This operation takes several minutes for large repos!
    
    **Example:**
    ```json
    {
      "owner": "python",
      "repo": "cpython",
      "force_rebuild": false
    }
    ```
    """
    try:
        pipeline = get_pipeline()
        
        if request.force_rebuild:
            from vector_store import delete_collection
            logger.warning(f"Force rebuild: clearing database...")
            delete_collection()
        
        logger.info(f"Building database for {request.owner}/{request.repo}...")
        success = pipeline.build_database(request.owner, request.repo)
        
        if success:
            stats = pipeline.get_stats()
            return BuildStatus(
                success=True,
                message=f"✅ Database built successfully",
                stats=stats
            )
        else:
            return BuildStatus(
                success=False,
                message="Failed to build database"
            )
    
    except Exception as e:
        logger.error(f"Build error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", response_model=DatabaseStats, tags=["Database"])
def get_statistics():
    """
    Get database statistics.
    
    **Returns:**
    - `total_chunks`: Number of code chunks in database
    - `unique_files`: Number of different files indexed
    - `files`: List of indexed files
    
    **Example:**
    ```json
    {
      "total_chunks": 1250,
      "unique_files": 85,
      "files": ["main.py", "utils.py", ...]
    }
    ```
    """
    try:
        stats = get_db_stats()
        return DatabaseStats(
            total_chunks=stats['total_chunks'],
            unique_files=stats['unique_files'],
            files=stats['files']
        )
    
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize pipeline on startup."""
    logger.info("🚀 FastAPI server starting...")
    logger.info(f"📡 API running on http://{API_HOST}:{API_PORT}")
    logger.info(f"📚 Interactive docs: http://{API_HOST}:{API_PORT}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("🛑 FastAPI server shutting down...")


# ============================================================================
# Run the Server
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    )
