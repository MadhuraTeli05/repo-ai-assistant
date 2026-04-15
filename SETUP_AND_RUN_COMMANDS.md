# 📋 Complete Step-by-Step Commands to Run The Project

This document provides exact commands to install, configure, and run the RAG project.

---

## PART 1: SETUP (One-Time)

### Step 1: Get GitHub Personal Access Token

**Visit this URL:**
```
https://github.com/settings/tokens
```

**Steps:**
1. Click "Generate new token" → "Generate new token (classic)"
2. Name it: `RAG_API_TOKEN`
3. Select scope: ✅ `public_repo`
4. Click "Generate token"
5. **Copy the token** (it starts with `ghp_`)
6. **Save it somewhere safe** - you won't see it again!

---

### Step 2: Open Terminal in Project Directory

**Windows PowerShell:**
```powershell
cd c:\Users\Viktus\OneDrive\Desktop\RAG_Project\repo-ai-assistant\backend
```

**Mac/Linux:**
```bash
cd ~/Desktop/RAG_Project/repo-ai-assistant/backend
```

---

### Step 3: Create .env Configuration File

Create a file named `.env` in `backend/backend/` folder:

**Option A: Copy from example (Recommended)**
```powershell
# Windows
cp backend\.env.example backend\.env

# Mac/Linux
cp backend/.env.example backend/.env
```

**Option B: Manual creation**

Create file: `backend/backend/.env`

With content:
```
GITHUB_TOKEN=your_token_here
GITHUB_OWNER=fastapi
GITHUB_REPO=fastapi
LOG_LEVEL=INFO
```

Replace `your_token_here` with your actual GitHub token (from Step 1).

---

### Step 4: Create Python Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Expected output: Your terminal should now show `(venv)` at the beginning.

---

### Step 5: Install All Dependencies

```bash
pip install -r backend/requirements.txt
```

This installs:
- chromadb (vector database)
- sentence-transformers (embeddings model)
- fastapi (REST API)
- uvicorn (API server)
- And 90+ other packages

**Time:** 5-10 minutes depending on internet speed.

---

### Step 6: Verify Installation

Run the health check:

```bash
cd backend
python check_system.py
```

Expected output: All checks should pass (green ✅)

If any fail, review the error messages and fix accordingly.

---

## PART 2: BUILD DATABASE

**This step downloads code from GitHub and creates embeddings. First run takes 10-30 minutes.**

### Option A: Build During Interactive Mode (Recommended)

Simply run:
```bash
python main.py
```

It will:
1. ✅ Check if database exists
2. ✅ If not, auto-build it
3. ✅ Then start interactive search mode

---

### Option B: Build Only (No Search)

```bash
python main.py --build
```

---

### Option C: Force Rebuild (Clear & Recreate)

```bash
python main.py --rebuild
```

---

### Progress Indicators

While building, you'll see:
```
📦 STEP 1: Initializing Database
   Repository: fastapi/fastapi

⚙️  Fetching files from GitHub...
✅ Fetched 2100 files

⚙️  Processing files and creating embeddings...
[Building...may take 20+ minutes]

✅ Database built successfully!
   Files processed: 1200
   Chunks created: 2850
   Embeddings stored: 2850
   Errors: 0
```

---

## PART 3: TEST THE APPLICATION

### Test 1: Interactive CLI Mode

```bash
python main.py
```

**What happens:**
1. Loads database (instant if already built)
2. Shows database stats
3. Asks for your question
4. Returns relevant code snippets

**Try searching:**
```
❓ Ask a question: How to handle errors?
```

Expected output:
```
✅ Found 5 relevant code chunks:

#1 - error_handler (function)
   File: fastapi/exception_handlers.py
   🎯 Relevance: 95%
   💻 Code:
   def error_handler(request, exc):
       """Handle exceptions"""
       ...
```

---

### Test 2: CLI Search Only

```bash
python main.py --search "How does routing work?"
```

Returns search results without building database first.

---

### Test 3: View Statistics

```bash
python main.py --stats
```

Expected output:
```
📊 Database Statistics
================================

📦 Total chunks: 2850
📁 Unique files: 120

📚 Files indexed:
   - fastapi/main.py
   - fastapi/routing.py
   - ...
```

---

### Test 4: REST API (Optional)

**Option A: Start API only**
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

**Option B: Start API with custom port**
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8080
```

Expected output:
```
INFO:     Started server process [1234]
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Test the API:**

Option 1: Visit in browser:
```
http://localhost:8000/docs
```

This opens interactive documentation where you can:
- ✅ Try search endpoint
- ✅ Build database
- ✅ View statistics

Option 2: Use curl:
```bash
# Search
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "error handling", "n_results": 5}'

# Get stats
curl -X GET "http://localhost:8000/stats"

# Build database
curl -X POST "http://localhost:8000/build" \
  -H "Content-Type: application/json" \
  -d '{"owner": "fastapi", "repo": "fastapi"}'
```

---

## PART 4: DIFFERENT USE CASES

### Use Case 1: One-Time Setup & Test

```bash
# 1. Setup
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Mac/Linux

# 2. Install
pip install -r backend/requirements.txt

# 3. Configure
# Create .env with GITHUB_TOKEN

# 4. Run
python main.py

# 5. Search
# Type your questions when prompted
```

---

### Use Case 2: Daily Development

```bash
# Terminal 1: Activate environment
cd backend
.\venv\Scripts\Activate.ps1

# Terminal 2: Run API
uvicorn api:app --reload

# Terminal 3: Test with curl
curl -X POST "http://localhost:8000/search" ...

# Terminal 4: Use CLI
python main.py --search "your question"
```

---

### Use Case 3: Process Different Repository

```bash
# Search in Django repo
python main.py --rebuild --owner django --repo django

# Then search
python main.py --search "how to use middleware?"
```

---

### Use Case 4: Integration with Other Code

```python
# In your Python project
from rag_pipeline import get_pipeline

pipeline = get_pipeline()

# Build if needed
pipeline.build_database("fastapi", "fastapi")

# Search
results = pipeline.search("error handling")

for match in results['matches']:
    print(f"{match['name']}: {match['similarity']}% relevant")
    print(match['code'])
```

---

## PART 5: TROUBLESHOOTING

### Problem: "GITHUB_TOKEN not found"

**Solution:**
1. Check .env file exists in `backend/backend/.env`
2. Check it contains: `GITHUB_TOKEN=ghp_...`
3. Restart the application

### Problem: "ModuleNotFoundError: No module named 'chromadb'"

**Solution:**
```bash
# Make sure venv is activated (should see (venv) in terminal)
pip install -r backend/requirements.txt
```

### Problem: "GitHub API Error 403"

**Reasons:**
- Invalid GITHUB_TOKEN
- Rate limit exceeded (wait 1 hour)
- Token doesn't have `public_repo` scope

**Solution:**
1. Generate new token from: https://github.com/settings/tokens
2. Update GITHUB_TOKEN in `.env`
3. Try again

### Problem: "First build takes 30+ minutes"

**Note:** This is NORMAL!
- FastAPI repo has 2000+ files
- Each file needs embedding generation
- First run is slow, subsequent runs are instant

**Speed up with smaller repo:**
```bash
python main.py --rebuild --owner pytorch --repo tutorials
```

### Problem: "Out of memory during build"

**Solutions:**
- Reduce `MAX_GITHUB_DEPTH` in `.env` (change from 2 to 1)
- Use smaller repository
- Close other applications
- Try again later

### Problem: "API won't start on port 8000"

**Solution:**
```bash
# Use different port
uvicorn api:app --reload --host 0.0.0.0 --port 8080

# Visit: http://localhost:8080/docs
```

---

## PART 6: FINAL VERIFICATION

Run this command to verify everything works:

```bash
python check_system.py
```

You should see:
```
✅ Python Version         PASS
✅ Dependencies           PASS
✅ Environment            PASS
✅ Module Imports         PASS
✅ File Structure         PASS
✅ Vector Database        PASS

Result: 6/6 checks passed
```

---

## PART 7: QUICK REFERENCE CHEATSHEET

```bash
# Activate environment
.\venv\Scripts\Activate.ps1            # Windows
source venv/bin/activate               # Mac/Linux

# Run application
python main.py                          # Interactive
python main.py --build                  # Build only
python main.py --search "question"      # Search only
python main.py --stats                  # Statistics
python main.py --rebuild                # Force rebuild

# API
uvicorn api:app --reload                # Start API
# Visit: http://localhost:8000/docs

# Verify
python check_system.py                  # Health check

# Debug
python main.py --stats                  # See what's in DB
grep -r "GITHUB_TOKEN" .env             # Check token is set
```

---

## ✅ SUCCESS INDICATORS

You'll know it's working when:

1. ✅ check_system.py shows all green
2. ✅ python main.py builds database without errors
3. ✅ You can ask questions and get code results
4. ✅ uvicorn starts API without errors
5. ✅ /docs shows Interactive API documentation

---

## 🎉 You're Done!

Your RAG application is now:
- ✅ Installed
- ✅ Configured
- ✅ Built
- ✅ Tested
- ✅ Ready to use!

**Next:** Try the interactive mode or start the API and explore!
