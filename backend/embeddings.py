"""
Embeddings Generation

This module converts text/code into numerical embeddings (vectors).
Embeddings allow semantic comparison of code - two similar code chunks
will have similar vectors even if they use different words.

The model used is "all-MiniLM-L6-v2":
- Lightweight (22MB, fast inference)
- 384-dimensional vectors (good balance of speed/accuracy)
- Pre-trained on sentence similarity tasks
"""

import logging
from sentence_transformers import SentenceTransformer
from config import EMBEDDINGS_MODEL

logger = logging.getLogger(__name__)

# Load model once at module import time (very important for performance)
# Loading the model multiple times would be extremely slow
try:
    model = SentenceTransformer(EMBEDDINGS_MODEL)
    logger.info(f"✅ Loaded embeddings model: {EMBEDDINGS_MODEL}")
except Exception as e:
    logger.error(f"❌ Failed to load embeddings model: {e}")
    raise


def get_embedding(text: str) -> list:
    """
    Convert text/code into an embedding vector.
    
    Embeddings are vectors (lists of numbers) that represent the semantic meaning
    of text. Two similar texts will have similar vectors.
    
    The embedding is a fixed-size vector (384 numbers) regardless of input length.
    
    Args:
        text (str): Code or text to convert to embedding
                   Can be any length (code snippet, function, question, etc.)
        
    Returns:
        list: Embedding vector of 384 numbers, each between -1 and 1
        
    Example:
        >>> text1 = "def add(a, b): return a + b"
        >>> text2 = "def sum_numbers(x, y): return x + y"
        >>> emb1 = get_embedding(text1)
        >>> emb2 = get_embedding(text2)
        >>> # emb1 and emb2 will be similar despite different variable names
        >>> print(len(emb1))  # 384
    """
    try:
        # Convert text to embedding vector (returns numpy array)
        embedding = model.encode(text)
        
        # Convert numpy array to Python list (for JSON serialization and storage)
        return embedding.tolist()
    
    except Exception as e:
        logger.error(f"Failed to generate embedding: {e}")
        raise