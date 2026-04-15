"""
Code Chunking Strategies

This module provides different ways to split code into meaningful chunks
for embedding. Proper chunking improves semantic search quality.
"""

import logging
from config import CHUNK_SIZE_LINES, CHUNK_OVERLAP

logger = logging.getLogger(__name__)


def chunk_by_lines(code_text, chunk_size=CHUNK_SIZE_LINES, overlap=CHUNK_OVERLAP):
    """
    Split code into overlapping chunks by line count.
    
    Useful for large files where a single function/class is very long.
    
    Args:
        code_text (str): Source code as string
        chunk_size (int): Number of lines per chunk
        overlap (int): Number of overlapping lines between chunks
        
    Returns:
        list: List of code chunks
        
    Example:
        >>> code = "line1\\nline2\\nline3\\nline4\\nline5"
        >>> chunks = chunk_by_lines(code, chunk_size=2, overlap=1)
        >>> print(len(chunks))  # 3 chunks
    """
    lines = code_text.split('\n')
    chunks = []
    
    if len(lines) <= chunk_size:
        return [code_text]
    
    step = chunk_size - overlap
    for i in range(0, len(lines), step):
        chunk_lines = lines[i:i + chunk_size]
        chunk = '\n'.join(chunk_lines)
        if chunk.strip():  # Don't store empty chunks
            chunks.append(chunk)
        
        # Stop if we've included all lines
        if i + chunk_size >= len(lines):
            break
    
    logger.debug(f"Split code into {len(chunks)} chunks by lines")
    return chunks


def chunk_by_functions(code_ast_nodes):
    """
    Create chunks where each function/class is a separate chunk.
    This is the default strategy used in parser.py
    
    Args:
        code_ast_nodes (list): List of AST nodes (functions/classes)
        
    Returns:
        list: List of code chunks
    """
    chunks = []
    for node in code_ast_nodes:
        chunks.append({
            "type": node.get("type"),
            "name": node.get("name"),
            "code": node.get("code"),
            "chunk_type": "function_or_class"
        })
    
    logger.debug(f"Created {len(chunks)} function/class chunks")
    return chunks


def chunk_by_tokens(code_text, max_tokens=512):
    """
    Split code into chunks based on approximate token count.
    Useful for respecting model input limits.
    
    ⚠️  This is a simple approximation (100 chars ≈ 30 tokens)
    For exact counts, use a tokenizer library.
    
    Args:
        code_text (str): Source code
        max_tokens (int): Maximum tokens per chunk
        
    Returns:
        list: List of code chunks
    """
    # Rough approximation: 100 chars = ~30 tokens
    chars_per_token = 3.5
    max_chars = int(max_tokens * chars_per_token)
    
    chunks = []
    
    if len(code_text) <= max_chars:
        return [code_text]
    
    # Split by trying to preserve line structure
    lines = code_text.split('\n')
    current_chunk = []
    current_chars = 0
    
    for line in lines:
        line_chars = len(line) + 1  # +1 for newline
        
        if current_chars + line_chars > max_chars and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_chars = line_chars
        else:
            current_chunk.append(line)
            current_chars += line_chars
    
    # Don't forget last chunk
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    logger.debug(f"Split code into {len(chunks)} token-based chunks (~{max_tokens} tokens each)")
    return chunks


def get_chunk_metadata(chunk, chunk_index, file_name, chunk_type="code"):
    """
    Create metadata dictionary for a chunk.
    
    Args:
        chunk (str or dict): The code chunk
        chunk_index (int): Index of chunk
        file_name (str): Name of source file
        chunk_type (str): Type of chunk (function, class, code, etc.)
        
    Returns:
        dict: Metadata for storage
    """
    if isinstance(chunk, dict):
        return {
            "type": chunk.get("type", chunk_type),
            "name": chunk.get("name", f"chunk_{chunk_index}"),
            "file": file_name,
            "chunk_index": chunk_index,
            "chunk_type": chunk.get("chunk_type", chunk_type)
        }
    
    return {
        "type": chunk_type,
        "name": f"chunk_{chunk_index}",
        "file": file_name,
        "chunk_index": chunk_index,
        "chunk_type": chunk_type
    }
