# RAG Code Search Project Documentation

## Overview

This project is a Retrieval-Augmented Generation (RAG) system for semantic code search across GitHub repositories. It combines a React frontend, a FastAPI backend, GitHub repository ingestion, AST-based Python code parsing, embeddings generation, ChromaDB vector storage, and OpenAI-powered answer generation.

## Prerequisites

### Software and tools required

| Tool | Version used in this workspace | Notes |
|---|---:|---|
| Python | 3.13.2 | Local runtime used in this workspace; backend code targets Python 3.8+ |
| Node.js | v22.21.1 | Local runtime used in this workspace |
| npm | 10.9.4 | Local npm version used in this workspace |
| Git | Any recent version | Required for cloning and source control |
| Web browser | Current stable browser | Used for the frontend and FastAPI docs |

### Required services and accounts

| Service | Purpose | Required |
|---|---|---|
| GitHub account | Access to repository contents through the GitHub API | Yes |
| GitHub personal access token | Authenticated repository access | Yes |
| OpenAI account/API key | LLM answer generation in the backend search flow | Yes for generated answers |

## Technologies Used

### Frontend

- React 18.2.0
- React DOM 18.2.0
- Vite 5.0.0
- Axios 1.6.0

### Backend

- FastAPI 0.135.2
- Uvicorn 0.42.0
- Pydantic 2.12.5
- Starlette 1.0.0
- Requests 2.33.0
- python-dotenv 1.2.2
- ChromaDB 1.5.5

### AI and LLM components

- Sentence-Transformers 5.3.0
- Transformers 5.4.0
- Torch 2.11.0
- OpenAI Python SDK 2.30.0
- Embeddings model: `all-MiniLM-L6-v2`
- Answer generation model: `gpt-5.4-mini`

### Vector database

- ChromaDB 1.5.5
- Persistent local storage under `backend/chroma_db/`

## Libraries and Packages

### Python packages

The backend dependencies are pinned in `backend/requirements.txt`.

| Package | Version |
|---|---:|
| annotated-doc | 0.0.4 |
| annotated-types | 0.7.0 |
| anyio | 4.13.0 |
| attrs | 26.1.0 |
| bcrypt | 5.0.0 |
| build | 1.4.2 |
| certifi | 2026.2.25 |
| charset-normalizer | 3.4.6 |
| chromadb | 1.5.5 |
| click | 8.3.1 |
| colorama | 0.4.6 |
| distro | 1.9.0 |
| durationpy | 0.10 |
| fastapi | 0.135.2 |
| filelock | 3.25.2 |
| flatbuffers | 25.12.19 |
| fsspec | 2026.2.0 |
| googleapis-common-protos | 1.73.1 |
| grpcio | 1.78.0 |
| h11 | 0.16.0 |
| hf-xet | 1.4.2 |
| httpcore | 1.0.9 |
| httptools | 0.7.1 |
| httpx | 0.28.1 |
| huggingface_hub | 1.8.0 |
| idna | 3.11 |
| importlib_metadata | 8.7.1 |
| importlib_resources | 6.5.2 |
| Jinja2 | 3.1.6 |
| jiter | 0.13.0 |
| joblib | 1.5.3 |
| jsonschema | 4.26.0 |
| jsonschema-specifications | 2025.9.1 |
| kubernetes | 35.0.0 |
| markdown-it-py | 4.0.0 |
| MarkupSafe | 3.0.3 |
| mdurl | 0.1.2 |
| mmh3 | 5.2.1 |
| mpmath | 1.3.0 |
| networkx | 3.6.1 |
| numpy | 2.4.3 |
| oauthlib | 3.3.1 |
| onnxruntime | 1.24.4 |
| openai | 2.30.0 |
| opentelemetry-api | 1.40.0 |
| opentelemetry-exporter-otlp-proto-common | 1.40.0 |
| opentelemetry-exporter-otlp-proto-grpc | 1.40.0 |
| opentelemetry-proto | 1.40.0 |
| opentelemetry-sdk | 1.40.0 |
| opentelemetry-semantic-conventions | 0.61b0 |
| orjson | 3.11.7 |
| overrides | 7.7.0 |
| packaging | 26.0 |
| protobuf | 6.33.6 |
| pybase64 | 1.4.3 |
| pydantic | 2.12.5 |
| pydantic-settings | 2.13.1 |
| pydantic_core | 2.41.5 |
| Pygments | 2.19.2 |
| PyPika | 0.51.1 |
| pyproject_hooks | 1.2.0 |
| python-dateutil | 2.9.0.post0 |
| python-dotenv | 1.2.2 |
| PyYAML | 6.0.3 |
| referencing | 0.37.0 |
| regex | 2026.2.28 |
| requests | 2.33.0 |
| requests-oauthlib | 2.0.0 |
| rich | 14.3.3 |
| rpds-py | 0.30.0 |
| safetensors | 0.7.0 |
| scikit-learn | 1.8.0 |
| scipy | 1.17.1 |
| sentence-transformers | 5.3.0 |
| setuptools | 81.0.0 |
| shellingham | 1.5.4 |
| six | 1.17.0 |
| sniffio | 1.3.1 |
| starlette | 1.0.0 |
| sympy | 1.14.0 |
| tenacity | 9.1.4 |
| threadpoolctl | 3.6.0 |
| tokenizers | 0.22.2 |
| torch | 2.11.0 |
| tqdm | 4.67.3 |
| transformers | 5.4.0 |
| typer | 0.24.1 |
| typing-inspection | 0.4.2 |
| typing_extensions | 4.15.0 |
| urllib3 | 2.6.3 |
| uvicorn | 0.42.0 |
| watchfiles | 1.1.1 |
| websocket-client | 1.9.0 |
| websockets | 16.0 |
| zipp | 3.23.0 |

### npm packages

The frontend dependencies are pinned in `frontend/package.json`.

| Package | Version |
|---|---:|
| react | ^18.2.0 |
| react-dom | ^18.2.0 |
| axios | ^1.6.0 |
| @types/react | ^18.2.0 |
| @types/react-dom | ^18.2.0 |
| @vitejs/plugin-react | ^4.2.0 |
| vite | ^5.0.0 |

## APIs Used

### Backend endpoints

| Method | Endpoint | Purpose | Notes |
|---|---|---|---|
| GET | `/` | API information | Returns basic metadata and documentation links |
| GET | `/health` | Health check | Used by the frontend startup check |
| POST | `/search` | Semantic code search | Accepts `query`, `n_results`, and optional `chat_history` |
| GET | `/search` | Semantic code search | Query-string version of search using `q` and `n_results` |
| POST | `/build` | Build or rebuild the repository database | Accepts `owner`, `repo`, and `force_rebuild` |
| GET | `/stats` | Database statistics | Returns total chunks, unique files, and file list |

### Endpoint notes

- There is no `/process-repo` endpoint in the current codebase.
- Repository processing is exposed through `POST /build` and the CLI entry point in `backend/main.py`.

### External APIs

| API | Purpose | Usage |
|---|---|---|
| GitHub Contents API | Lists repository files and folders | `https://api.github.com/repos/{owner}/{repo}/contents/{path}` |
| GitHub raw file downloads | Downloads file content | Uses the `download_url` returned by the GitHub Contents API |
| OpenAI Responses API | Generates the final natural-language answer | Called through the OpenAI Python SDK with `OPENAI_API_KEY` |

## Environment Setup

### Backend environment variables

Configure these values in `backend/.env`.

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `GITHUB_TOKEN` | Yes | None | GitHub API authentication |
| `OPENAI_API_KEY` | Yes for answer generation | None | OpenAI model access for generated answers |
| `GITHUB_OWNER` | No | `fastapi` | Default repository owner |
| `GITHUB_REPO` | No | `fastapi` | Default repository name |
| `MAX_GITHUB_DEPTH` | No | `2` | Maximum recursive folder traversal depth |
| `SKIP_FOLDERS` | No | `docs,tests,.github,images,examples,build,dist` | GitHub folders to skip |
| `GITHUB_REQUEST_TIMEOUT` | No | `30` | GitHub API request timeout in seconds |
| `GITHUB_REQUEST_DELAY` | No | `0.2` | Delay between GitHub API requests |
| `CHROMA_DB_PATH` | No | `chroma_db` | Local ChromaDB storage path |
| `CHROMA_COLLECTION_NAME` | No | `repo_chunks` | ChromaDB collection name |
| `EMBEDDINGS_MODEL` | No | `all-MiniLM-L6-v2` | Embedding model name |
| `EMBEDDINGS_DIMENSION` | No | `384` | Embedding vector size |
| `SEARCH_RESULTS_COUNT` | No | `5` | Default search result count |
| `SIMILARITY_THRESHOLD` | No | `0.0` | Optional similarity filter |
| `API_HOST` | No | `0.0.0.0` | FastAPI host binding |
| `API_PORT` | No | `8000` | FastAPI port |
| `API_RELOAD` | No | `True` | Auto-reload for local development |
| `SUPPORTED_EXTENSIONS` | No | `.py` | File extensions to process |
| `MAX_FILE_SIZE` | No | `1048576` | Maximum file size in bytes |
| `CHUNK_SIZE_LINES` | No | `50` | Line-based chunk size |
| `CHUNK_OVERLAP` | No | `10` | Line overlap between chunks |
| `LOG_LEVEL` | No | `INFO` | Logging level |

### Frontend environment variables

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `VITE_API_URL` | No | `http://localhost:8000` | Backend API base URL template |

### API keys needed

- GitHub personal access token for repository access.
- OpenAI API key for answer generation in the search flow.

## Project Architecture

### High-level flow

1. The frontend collects a GitHub owner/repository and sends a build request to the backend.
2. The backend fetches repository contents from GitHub.
3. Python source files are parsed and chunked into function/class segments or line-based segments when needed.
4. Each chunk is converted into an embedding with `all-MiniLM-L6-v2`.
5. Embeddings and metadata are stored in ChromaDB.
6. During search, the user query is embedded and compared against the vector database.
7. The backend returns ranked matches and an OpenAI-generated answer.
8. The frontend renders the answer, similarity scores, and code previews.

### Data flow summary

`Frontend -> FastAPI backend -> GitHub API -> parser/chunking -> embeddings -> ChromaDB -> search -> OpenAI response -> frontend`

## Folder Structure Overview

### Root

- `backend/` - Python backend, API, pipeline, database, and dependencies
- `frontend/` - React/Vite client application
- `quickstart.py` - Setup helper script
- `SETUP_AND_RUN_COMMANDS.md` - Detailed setup commands
- `IMPLEMENTATION_COMPLETE.md` - Project completion summary

### Backend

- `api.py` - FastAPI REST API
- `main.py` - CLI entry point
- `rag_pipeline.py` - Core orchestration layer
- `github_service.py` - GitHub API integration
- `parser.py` - Python AST parsing
- `chunking.py` - Code chunking strategies
- `embeddings.py` - Embedding generation
- `vector_store.py` - ChromaDB persistence and search
- `config.py` - Environment-based configuration
- `check_system.py` - System verification script
- `requirements.txt` - Python dependency list
- `README.md` - Backend setup guide
- `chroma_db/` - Persistent vector database files

### Frontend

- `index.html` - Vite entry HTML
- `package.json` - npm dependencies and scripts
- `vite.config.js` - Vite build configuration
- `src/` - React application source
  - `App.jsx` - Main application shell
  - `main.jsx` - React bootstrap
  - `components/` - UI components for repository input, search, and results
  - `services/api.js` - Frontend API wrapper
  - CSS files for layout and component styling

## Setup and Run Instructions

### Backend setup

1. Change into the backend directory.
2. Create and activate a Python virtual environment.
3. Install dependencies from `backend/requirements.txt`.
4. Copy `backend/.env.example` to `backend/.env`.
5. Add at least `GITHUB_TOKEN` and `OPENAI_API_KEY` to `backend/.env`.
6. Run `python main.py` for interactive mode, or use the API server.

### Backend commands

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

To run the API server:

```powershell
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Frontend setup

1. Change into the frontend directory.
2. Install npm dependencies.
3. Optionally copy `frontend/.env.example` to `frontend/.env`.
4. Start the Vite development server.

### Frontend commands

```powershell
cd frontend
npm install
npm run dev
```

### Common run modes

- Interactive CLI: `python backend/main.py`
- Build database only: `python backend/main.py --build`
- Force rebuild: `python backend/main.py --rebuild`
- Search only: `python backend/main.py --search "your query"`
- Database stats: `python backend/main.py --stats`

### Verification

- FastAPI docs: `http://localhost:8000/docs`
- Backend health check: `http://localhost:8000/health`
- Frontend dev server: `http://localhost:5173`

## Additional Notes

- The repository includes a persistent local ChromaDB database under `backend/chroma_db/`.
- The backend search endpoint accepts optional chat history, while the frontend currently performs standard query and result-count requests.
- The frontend API wrapper currently targets `http://localhost:8000`.
