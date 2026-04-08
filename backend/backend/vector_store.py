# Import ChromaDB (vector database library)
import chromadb


# Create a persistent client
# "chroma_db" → folder where data will be stored permanently
client = chromadb.PersistentClient(path="chroma_db")


# Create or get a collection (like a table in SQL)
# "repo_chunks" will store all embeddings of code
collection = client.get_or_create_collection(name="repo_chunks")


def store_embedding(chunk_id, embedding, metadata, document):
    """
    Store embedding in the vector database

    Parameters:
    chunk_id (str): Unique ID for each code chunk
    embedding (list): Vector representation of the code
    metadata (dict): Additional information (name, file, type)
    """

    # Add data to the database
    collection.upsert(
        ids=[chunk_id],              # Unique identifier
        embeddings=[embedding],      # Vector (meaning of code)
        metadatas=[metadata],         # Extra info about code
        documents=[document]         # Original code text (optional, can be used for retrieval)
    )

           
                    

def view_data():
    """
    View stored data in the database (for debugging)
    """

    # Fetch data from database
    # include=["embeddings"] is IMPORTANT because embeddings are not returned by default
    data = collection.get(include=["embeddings", "metadatas"])

    # Print total number of stored entries
    print("\nTotal entries:", len(data["ids"]))

    # Show first 3 entries for readability
    for i in range(min(3, len(data["ids"]))):

        print("\n--- Entry", i, "---")

        # Print unique ID
        print("ID:", data["ids"][i])

        # Print metadata (function/class info)
        print("Metadata:", data["metadatas"][i])

        # Print only first 5 values of embedding (because full vector is very large)
        if data["embeddings"] is not None:
            print("Embedding (first 5 values):", data["embeddings"][i][:5])

"""Takes query embedding
↓
Finds closest stored embeddings
↓
Returns best matches"""

def search_similar(query_embedding, n_results=3):
    """
    Search similar embeddings from database
    """

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["metadatas", "documents","distances"]
    )

    return results

def is_db_empty():
    data=collection.get()
    return len(data["ids"]) == 0
