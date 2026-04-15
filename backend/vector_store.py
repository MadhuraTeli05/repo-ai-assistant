"""
Vector Store Management

This module manages ChromaDB, a vector database for storing and searching embeddings.

ChromaDB automatically:
- Stores embeddings (vectors representing code meaning)
- Persists data on disk in "chroma_db/" folder
- Provides fast semantic search using vector similarity
"""

import logging
import chromadb
from config import CHROMA_DB_PATH, CHROMA_COLLECTION_NAME, SEARCH_RESULTS_COUNT

logger = logging.getLogger(__name__)

# Create persistent client - stores data in folder on disk
# This means embeddings survive even after the app stops
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Create or get a collection (like a SQL table)
# Each collection stores embeddings for one set of documents
collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}  # Use cosine similarity for comparison
)

logger.info(f"✅ Connected to vector store: {CHROMA_DB_PATH}/{CHROMA_COLLECTION_NAME}")


def store_embedding(chunk_id: str, embedding: list, metadata: dict, document: str) -> bool:
    """
    Store an embedding in the vector database.
    
    This function saves:
    - The embedding vector (numerical representation of code meaning)
    - Metadata (type, name, file, chunk index)
    - Original code text (for retrieval)
    
    Args:
        chunk_id (str): Unique identifier for this chunk (e.g., "file.py_0_function_name")
        embedding (list): Vector of 384 numbers representing code meaning
        metadata (dict): Extra information about the chunk {"name": "...", "type": "...", "file": "..."}
        document (str): Original source code text
        
    Returns:
        bool: True if successful
        
    Example:
        >>> embedding = [0.1, 0.2, 0.3, ...]  # 384 numbers
        >>> store_embedding(
        ...     chunk_id="parser.py_0_extract_chunks",
        ...     embedding=embedding,
        ...     metadata={"name": "extract_chunks", "type": "function", "file": "parser.py"},
        ...     document="def extract_chunks(code):\\n    ..."
        ... )
    """
    try:
        collection.upsert(
            ids=[chunk_id],           # Unique ID
            embeddings=[embedding],   # Vector (meaning representation)
            metadatas=[metadata],     # Searchable metadata
            documents=[document]      # Source text (for context in results)
        )
        logger.debug(f"Stored embedding: {chunk_id}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to store embedding {chunk_id}: {e}")
        return False


def search_similar(query_embedding: list, n_results: int = SEARCH_RESULTS_COUNT) -> dict:
    """
    Find similar code chunks using semantic similarity.
    
    This searches the database using vector distance:
    - Lower distance = more similar
    - Higher similarity score (1 - distance) = better match
    
    Args:
        query_embedding (list): Embedding vector of question (384 numbers)
        n_results (int): How many results to return
        
    Returns:
        dict: Results with structure:
            {
                "ids": [[id1, id2, ...]],
                "documents": [[code1, code2, ...]],
                "metadatas": [[meta1, meta2, ...]],
                "distances": [[0.1, 0.2, ...]]  # Lower = better
            }
            
    Example:
        >>> results = search_similar(query_embedding, n_results=5)
        >>> for i, code in enumerate(results["documents"][0]):
        ...     print(f"Result {i+1}: {code[:100]}...")
    """
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["metadatas", "documents", "distances"]
        )
        logger.debug(f"Found {len(results['ids'][0]) if results['ids'] else 0} similar chunks")
        return results
    
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return {"ids": [], "documents": [], "metadatas": [], "distances": []}


def view_data(limit: int = 3) -> None:
    """
    Display sample data from vector database (for debugging).
    
    Args:
        limit (int): Number of samples to display
    """
    try:
        data = collection.get(include=["embeddings", "metadatas"])
        
        print("\n" + "="*70)
        print("VECTOR DATABASE CONTENTS")
        print("="*70)
        print(f"\n✅ Total stored chunks: {len(data['ids'])}\n")
        
        if len(data['ids']) == 0:
            print("Database is empty")
            print("="*70 + "\n")
            return
        
        # Show first N entries
        for i in range(min(limit, len(data['ids']))):
            print(f"--- Sample {i+1} ---")
            print(f"ID: {data['ids'][i]}")
            print(f"Metadata: {data['metadatas'][i]}")
            
            # Show first 5 embedding values (full vector has 384 values)
            if data['embeddings'] and data['embeddings'][i]:
                print(f"Embedding (first 5 of 384): {data['embeddings'][i][:5]}")
            print()
        
        print("="*70 + "\n")
    
    except Exception as e:
        logger.error(f"Failed to view data: {e}")


def is_db_empty() -> bool:
    """
    Check if database is empty.
    
    Returns:
        bool: True if no embeddings stored, False otherwise
    """
    try:
        data = collection.get()
        is_empty = len(data["ids"]) == 0
        logger.debug(f"Database empty check: {is_empty}")
        return is_empty
    except Exception as e:
        logger.error(f"Failed to check if database empty: {e}")
        return True


def get_db_stats() -> dict:
    """
    Get statistics about the database.
    
    Returns:
        dict: Statistics including total entries, sample files
    """
    try:
        data = collection.get()
        files = set(
            meta.get("file", "unknown") 
            for meta in data.get("metadatas", [])
        )
        
        return {
            "total_chunks": len(data["ids"]),
            "unique_files": len(files),
            "files": list(files)
        }
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {"total_chunks": 0, "unique_files": 0, "files": []}


def delete_collection(confirm: bool = True) -> bool:
    """
    Delete entire collection (useful for rebuilding).
    
    ⚠️  WARNING: This deletes ALL stored embeddings!
    
    Args:
        confirm (bool): Require confirmation
        
    Returns:
        bool: True if deleted
    """
    try:
        if confirm:
            logger.warning(f"⚠️  Deleting entire collection: {CHROMA_COLLECTION_NAME}")
        
        client.delete_collection(name=CHROMA_COLLECTION_NAME)
        logger.info("✅ Collection deleted")
        
        # Recreate empty collection
        global collection
        collection = client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("✅ New empty collection created")
        return True
    
    except Exception as e:
        logger.error(f"Failed to delete collection: {e}")
        return False
