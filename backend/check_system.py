#!/usr/bin/env python3
"""
System Check Script for RAG Application

Verifies that all dependencies, configuration, and basics are working correctly.
Run this after installation to ensure everything is set up properly.

Usage:
    python check_system.py
"""

import sys
import os
import importlib
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*70}")
    print(f"{text}")
    print(f"{'='*70}{RESET}")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"ℹ️  {text}")

def check_python_version():
    """Check Python version."""
    print_header("1️⃣  Python Version")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} (requires 3.8+)")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    print_header("2️⃣  Dependencies")
    
    required_packages = {
        'chromadb': 'Vector database',
        'sentence_transformers': 'Text embedding model',
        'fastapi': 'REST API framework',
        'uvicorn': 'ASGI server',
        'requests': 'HTTP library',
        'python_dotenv': 'Environment variables',
        'astroid': 'Code analysis (optional)',
    }
    
    all_good = True
    for package, description in required_packages.items():
        try:
            importlib.import_module(package)
            print_success(f"{package:30} - {description}")
        except ImportError:
            print_error(f"{package:30} - NOT INSTALLED")
            all_good = False
    
    return all_good

def check_env_file():
    """Check if .env file exists and has GitHub token."""
    print_header("3️⃣  Environment Configuration")
    
    env_files = [
        'backend/.env',
        'backend/backend/.env',
        '.env'
    ]
    
    env_exists = False
    has_token = False
    
    for env_file in env_files:
        if os.path.exists(env_file):
            print_success(f"Found: {env_file}")
            env_exists = True
            
            # Check for GITHUB_TOKEN
            with open(env_file, 'r') as f:
                content = f.read()
                if 'GITHUB_TOKEN' in content:
                    # Check if it has a value
                    for line in content.split('\n'):
                        if line.startswith('GITHUB_TOKEN=') and '=' in line:
                            token_part = line.split('=')[1].strip()
                            if token_part and token_part != 'ghp_your_token_here_replace_me':
                                print_success("GITHUB_TOKEN is set")
                                has_token = True
                            else:
                                print_error("GITHUB_TOKEN is empty or placeholder")
                            break
            break
    
    if not env_exists:
        print_error(".env file not found!")
        print_info("Create .env file with: GITHUB_TOKEN=your_token_here")
    
    if not has_token:
        print_warning("GITHUB_TOKEN is missing or invalid")
        print_info("Get token from: https://github.com/settings/tokens")
    
    return env_exists and has_token

def check_module_imports():
    """Check if project modules can be imported."""
    print_header("4️⃣  Project Modules")
    
    modules = [
        'config',
        'embeddings',
        'parser',
        'github_service',
        'vector_store',
        'chunking',
        'rag_pipeline',
    ]
    
    all_good = True
    for module in modules:
        try:
            importlib.import_module(module)
            print_success(f"{module:30} - Importable")
        except ImportError as e:
            print_error(f"{module:30} - Import failed: {e}")
            all_good = False
        except Exception as e:
            print_error(f"{module:30} - Error: {e}")
            all_good = False
    
    return all_good

def check_files_exist():
    """Check if all required files exist."""
    print_header("5️⃣  File Structure")
    
    required_files = [
        'main.py',
        'api.py',
        'config.py',
        'embeddings.py',
        'parser.py',
        'github_service.py',
        'vector_store.py',
        'chunking.py',
        'rag_pipeline.py',
        'requirements.txt',
        '.env.example',
    ]
    
    all_good = True
    for filename in required_files:
        if os.path.exists(filename):
            print_success(f"{filename:30} - Present")
        else:
            print_error(f"{filename:30} - MISSING")
            all_good = False
    
    return all_good

def check_chromadb():
    """Check ChromaDB connectivity."""
    print_header("6️⃣  Vector Database")
    
    try:
        import chromadb
        from config import CHROMA_DB_PATH, CHROMA_COLLECTION_NAME
        
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)
        
        data = collection.get()
        count = len(data['ids']) if data['ids'] else 0
        
        print_success(f"ChromaDB accessible at: {CHROMA_DB_PATH}")
        print_success(f"Current chunks in database: {count}")
        
        if count == 0:
            print_info("Database is empty - needs to be built")
        
        return True
    
    except Exception as e:
        print_error(f"ChromaDB error: {e}")
        return False

def check_embeddings_model():
    """Check if embeddings model can be loaded."""
    print_header("7️⃣  Embeddings Model")
    
    try:
        from sentence_transformers import SentenceTransformer
        from config import EMBEDDINGS_MODEL
        
        print_info(f"Loading model: {EMBEDDINGS_MODEL}...")
        print_info("(This might take a moment on first run...)")
        
        model = SentenceTransformer(EMBEDDINGS_MODEL)
        
        # Test encoding
        test_text = "def hello(): pass"
        embedding = model.encode(test_text)
        
        print_success(f"Model loaded and working!")
        print_success(f"Embedding dimension: {len(embedding)}")
        
        return True
    
    except Exception as e:
        print_error(f"Embeddings error: {e}")
        print_info("The model will be downloaded on first use")
        return False

def main():
    """Run all checks."""
    print(f"\n{BLUE}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║         RAG APPLICATION - SYSTEM HEALTH CHECK                      ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(RESET)
    
    results = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "Environment": check_env_file(),
        "Module Imports": check_module_imports(),
        "File Structure": check_files_exist(),
        "Vector Database": check_chromadb(),
        # "Embeddings Model": check_embeddings_model(),  # Optional (slow)
    }
    
    print_header("📊 SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check, result in results.items():
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {check:30} {status}")
    
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        print(f"\n{GREEN}✅ All systems operational!{RESET}")
        print(f"\n{BLUE}Next steps:{RESET}")
        print("  1. python main.py                  # Run interactive mode")
        print("  2. python main.py --build          # Build database")
        print("  3. python main.py --search query   # Test search")
        print("  4. uvicorn api:app --reload        # Start REST API")
        return 0
    else:
        print(f"\n{RED}⚠️  Some checks failed. See above for details.{RESET}")
        print(f"\nCommon fixes:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Create .env file: cp .env.example .env")
        print("  3. Add GitHub token: GITHUB_TOKEN=ghp_...")
        print("  4. Ensure you're in the backend/backend/ directory")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
