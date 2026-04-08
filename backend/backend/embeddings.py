# Import the SentenceTransformer class
# This library provides pre-trained models to convert text into embeddings (vectors)
from sentence_transformers import SentenceTransformer


# Load the model ONLY ONCE (very important for performance)
# "all-MiniLM-L6-v2" is a lightweight model that converts text into 384-dimensional vectors
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text):
    """
    Convert input text into an embedding vector

    Parameters:
    text (str): The text/code to be converted into numerical representation

    Returns:
    list: A list of numbers (embedding vector)
    """

    # Convert text into embedding (numpy array of 384 numbers)
    embedding = model.encode(text)

    # Convert numpy array → Python list (for storing in database)
    return embedding.tolist()