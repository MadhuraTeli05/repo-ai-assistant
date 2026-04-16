"""
RAG Pipeline Orchestration

This module orchestrates the complete RAG pipeline:
1. Fetch code from GitHub
2. Parse and chunk code
3. Generate embeddings
4. Store in vector database
5. Enable semantic search

This abstraction makes it easy to reuse the pipeline across different services.
"""

from openai import OpenAI
import os
import logging
from typing import Dict

from github_service import fetch_repo_files, fetch_file_content
from parser import extract_python_chunks
from embeddings import get_embedding
from vector_store import (
    store_embedding,
    search_similar,
    is_db_empty,
    view_data,
    delete_collection,
)
from chunking import chunk_by_lines
from config import (
    SUPPORTED_EXTENSIONS,
    MAX_FILE_SIZE,
    SKIP_FOLDERS,
    CHUNK_SIZE_LINES,
    CHUNK_OVERLAP,
)

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class RAGPipeline:
    """
    Retrieval-Augmented Generation Pipeline

    Manages the complete workflow from GitHub repo to semantic search.
    """

    def __init__(self, collection_name: str = "repo_chunks"):
        """
        Initialize RAG pipeline.

        Args:
            collection_name (str): ChromaDB collection to use
        """
        self.collection_name = collection_name
        self.stats = {
            "files_fetched": 0,
            "files_processed": 0,
            "chunks_created": 0,
            "embeddings_stored": 0,
            "errors": 0,
        }
        logger.info(f"✅ RAG Pipeline initialized (collection: {collection_name})")

    def build_database(
        self,
        owner: str,
        repo: str,
        force_rebuild: bool = False
    ) -> bool:
        """
        Build embeddings database from GitHub repository.

        Args:
            owner (str): GitHub repo owner
            repo (str): GitHub repo name
            force_rebuild (bool): Clear existing data and rebuild

        Returns:
            bool: True if successful
        """
        try:
            if force_rebuild:
                logger.warning("🔄 Force rebuild: clearing existing database...")
                delete_collection()
            elif not is_db_empty():
                logger.info("⚡ Database already exists, skipping rebuild")
                return True

            logger.info(f"📥 Building database for {owner}/{repo}...")

            # Step 1: Fetch files from GitHub
            logger.info("Step 1: Fetching files from GitHub...")
            files = fetch_repo_files(owner, repo)
            self.stats["files_fetched"] = len(files)

            if not files:
                logger.error("❌ No files fetched from GitHub!")
                return False

            logger.info(f"✅ Fetched {len(files)} files")

            # Step 2: Process each file
            logger.info("Step 2: Processing files and creating embeddings...")
            for file_index, file in enumerate(files):
                try:
                    # Only process supported file types
                    if not any(file["name"].endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                        continue

                    # Skip unwanted folders
                    if any(skip in file["path"] for skip in SKIP_FOLDERS):
                        logger.debug(f"Skipped: {file['name']} (in skip list)")
                        continue

                    logger.info(f"[{file_index + 1}] Processing: {file['name']}")

                    # Download file content
                    code = fetch_file_content(file["download_url"])
                    if not code:
                        logger.warning(f"⚠️ Failed to fetch content for {file['name']}")
                        self.stats["errors"] += 1
                        continue

                    # Check file size
                    if len(code.encode("utf-8")) > MAX_FILE_SIZE:
                        logger.warning(f"⚠️ File too large: {file['name']} (skipped)")
                        self.stats["errors"] += 1
                        continue

                    self.stats["files_processed"] += 1

                    # Step 3: Extract functions and classes
                    chunks = extract_python_chunks(code)

                    # If too large, split by lines
                    if len(code.split("\n")) > CHUNK_SIZE_LINES:
                        line_chunks = chunk_by_lines(code, CHUNK_SIZE_LINES, CHUNK_OVERLAP)
                        chunks = []
                        for i, chunk in enumerate(line_chunks):
                            chunks.append({
                                "type": "code_segment",
                                "name": f"{file['name']}_segment_{i}",
                                "code": chunk
                            })

                    if not chunks:
                        logger.debug(f"No chunks extracted from {file['name']}")
                        continue

                    # Step 4: Generate embeddings and store
                    for chunk_index, chunk in enumerate(chunks):
                        try:
                            code_text = chunk.get("code", "")
                            if not code_text.strip():
                                continue

                            embedding = get_embedding(code_text)

                            metadata = {
                                "type": chunk.get("type"),
                                "name": chunk.get("name"),
                                "file": file["name"],
                                "file_path": file["path"],
                                "chunk_index": chunk_index,
                            }

                            chunk_id = f"{file['path']}_{chunk_index}_{chunk.get('name', 'chunk')}"
                            chunk_id = chunk_id.replace("/", "_").replace(".", "_")

                            store_embedding(
                                chunk_id=chunk_id,
                                embedding=embedding,
                                metadata=metadata,
                                document=code_text
                            )

                            self.stats["embeddings_stored"] += 1
                            self.stats["chunks_created"] += 1

                            logger.debug(f"  ✓ Stored: {chunk.get('name', 'chunk')}")

                        except Exception as e:
                            logger.error(f"Error processing chunk: {e}")
                            self.stats["errors"] += 1
                            continue

                except Exception as e:
                    logger.error(f"Error processing file {file['name']}: {e}")
                    self.stats["errors"] += 1
                    continue

            logger.info("\n" + "=" * 60)
            logger.info("✅ Database built successfully!")
            logger.info(f"   Files fetched: {self.stats['files_fetched']}")
            logger.info(f"   Files processed: {self.stats['files_processed']}")
            logger.info(f"   Chunks created: {self.stats['chunks_created']}")
            logger.info(f"   Embeddings stored: {self.stats['embeddings_stored']}")
            logger.info(f"   Errors: {self.stats['errors']}")
            logger.info("=" * 60 + "\n")

            return True

        except Exception as e:
            logger.error(f"❌ Failed to build database: {e}")
            return False

    def search(
        self,
        query: str,
        n_results: int = 5,
        include_distances: bool = True,
        chat_history=None
    ) -> Dict:
        """
        Search for similar code chunks and generate an LLM answer.
        """
        if chat_history is None:
            chat_history = []

        def format_history(history):
            if not history:
                return ""
            return "\n".join(
                [f"User: {h['question']}\nAI: {h['answer']}" for h in history]
            )

        try:
            logger.info(f"🔍 Searching for: {query[:50]}...")

            # Convert query to embedding
            query_embedding = get_embedding(query)

            # Search vector database
            raw_results = search_similar(query_embedding, n_results)

            # Format results
            formatted_results = {
                "query": query,
                "total_matches": len(raw_results["ids"][0]) if raw_results["ids"] else 0,
                "matches": []
            }

            if not raw_results["ids"] or not raw_results["ids"][0]:
                logger.warning("No matches found")
                return {
                    "query": query,
                    "answer": "Not found in repository",
                    "matches": []
                }

            for i, chunk_id in enumerate(raw_results["ids"][0]):
                match = {
                    "rank": i + 1,
                    "id": chunk_id,
                    "name": raw_results["metadatas"][0][i].get("name"),
                    "type": raw_results["metadatas"][0][i].get("type"),
                    "file": raw_results["metadatas"][0][i].get("file"),
                    "code": raw_results["documents"][0][i] if raw_results["documents"] else "",
                }

                if include_distances and raw_results.get("distances"):
                    distance = raw_results["distances"][0][i]
                    match["similarity"] = max(0, 1 - distance)

                formatted_results["matches"].append(match)

            # Build context from top retrieved chunks
            top_chunks = [m["code"] for m in formatted_results["matches"][:5]]
            context = "\n\n".join(top_chunks)
            history_text = format_history(chat_history)

            prompt = f"""
You are an expert code assistant.

Use the repository context and conversation history to answer clearly.

Rules:
- Prefer direct evidence from the retrieved code.
- If the answer is not explicit, make a careful inference from the code.
- For follow-up questions, use the conversation history.
- Only say "Not found in repository" if the context is truly insufficient.

Conversation History:
{history_text}

Context:
{context}

Current Question:
{query}

Answer:
"""

            try:
                response = client.responses.create(
                    model="gpt-5.4-mini",
                    input=prompt
                )
                answer = response.output_text
            except Exception as e:
                logger.error(f"LLM error: {e}")
                answer = "Error generating answer"

            logger.info(f"✅ Found {len(formatted_results['matches'])} matches")
            return {
                "query": query,
                "answer": answer,
                "matches": formatted_results["matches"]
            }

        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return {"error": str(e), "matches": []}

    def get_stats(self) -> Dict:
        """Get pipeline statistics."""
        return self.stats.copy()

    def view_database(self):
        """Display sample data from database (for debugging)."""
        view_data()


# Singleton instance for easy access
_pipeline_instance = None


def get_pipeline(collection_name: str = "repo_chunks") -> RAGPipeline:
    """
    Get or create RAG pipeline instance.

    Args:
        collection_name (str): ChromaDB collection name

    Returns:
        RAGPipeline: Pipeline instance
    """
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = RAGPipeline(collection_name)
    return _pipeline_instance