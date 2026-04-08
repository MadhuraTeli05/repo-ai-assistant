print("PROGRAM STARTED")     #debug 
from github_service import fetch_repo_files, fetch_file_content   #Uses functions from gihub_service.py file
from parser import extract_python_chunks
from embeddings import get_embedding
# from vector_store import store_embedding
from vector_store import store_embedding, view_data,is_db_empty



owner = "fastapi"
repo = "fastapi"

if is_db_empty():
    print("\nDB is empty → Building database...")

    files = fetch_repo_files(owner, repo)

    print("\nTotal files fetched:", len(files))

    for file in files:

        print("Checking:", file["name"])

        if file["type"] == "file" and file["name"].endswith(".py"):

            print(f"\nProcessing File: {file['name']}")

            code = fetch_file_content(file["download_url"])

            if code:
                chunks = extract_python_chunks(code)

                for i, chunk in enumerate(chunks):

                    text = chunk["code"]

                    embedding = get_embedding(text)

                    store_embedding(
                        chunk_id=f"{file['path']}_{i}",
                        embedding=embedding,
                        metadata={
                            "type": chunk["type"],
                            "name": chunk["name"],
                            "file": file["name"]
                        },
                        document=chunk["code"]
                    )

                    print(f"Stored: {chunk['name']}")

    print("\n✅ Database created successfully!")

else:
    print("\n⚡ Database already exists → Skipping processing")   

print("\n===== VIEWING STORED DATA =====")                  
view_data()                                                 #DEBUG function call to view the data stored in the vector database, prints total entries and sample metadata and embedding values

"""Your system understood the question
↓
Matched meaning (not keywords!)
↓
Returned relevant code"""

from vector_store import search_similar

print("\n===== ASK QUESTION =====")

query = input("Enter your question: ")

# Convert question → embedding
query_embedding = get_embedding(query)

# Search database
results = search_similar(query_embedding)

print("\n===== SEARCH RESULTS =====")

for i in range(len(results["ids"][0])):
    print("\nResult", i + 1)
    print("ID:", results["ids"][0][i])
    print("Metadata:", results["metadatas"][0][i])   
    print("PROGRAM STARTED")     #debug 
from github_service import fetch_repo_files, fetch_file_content   #Uses functions from gihub_service.py file
from parser import extract_python_chunks
from embeddings import get_embedding
# from vector_store import store_embedding
from vector_store import store_embedding, view_data,is_db_empty



owner = "fastapi"
repo = "fastapi"

if is_db_empty():
    print("\nDB is empty → Building database...")

    files = fetch_repo_files(owner, repo)

    print("\nTotal files fetched:", len(files))

    for file in files:

        print("Checking:", file["name"])

        if file["type"] == "file" and file["name"].endswith(".py"):

            print(f"\nProcessing File: {file['name']}")

            code = fetch_file_content(file["download_url"])

            if code:
                chunks = extract_python_chunks(code)

                for i, chunk in enumerate(chunks):

                    text = chunk["code"]

                    embedding = get_embedding(text)

                    store_embedding(
                        chunk_id=f"{file['path']}_{i}",
                        embedding=embedding,
                        metadata={
                            "type": chunk["type"],
                            "name": chunk["name"],
                            "file": file["name"]
                        },
                        document=chunk["code"]
                    )

                    print(f"Stored: {chunk['name']}")

    print("\n✅ Database created successfully!")

else:
    print("\n⚡ Database already exists → Skipping processing")   

print("\n===== VIEWING STORED DATA =====")                  
view_data()                                                 #DEBUG function call to view the data stored in the vector database, prints total entries and sample metadata and embedding values

"""Your system understood the question
↓
Matched meaning (not keywords!)
↓
Returned relevant code"""

from vector_store import search_similar

print("\n===== ASK QUESTION =====")

query = input("Enter your question: ")

# Convert question → embedding
query_embedding = get_embedding(query)

# Search database
results = search_similar(query_embedding)

print("\n===== SEARCH RESULTS =====")

for i in range(len(results["ids"][0])):
    print("\nResult", i + 1)
    print("ID:", results["ids"][0][i])
    print("Metadata:", results["metadatas"][0][i])   
    print("Distance:", results["distances"][0][i])

    if results["documents"] and results["documents"][0][i]:
        print("Code:\n", results["documents"][0][i][:500])   # first 500 chars
        
        