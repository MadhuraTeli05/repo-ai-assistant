#!/usr/bin/env python3
"""
Quick Start Setup Script

This script guides you through the complete setup process:
1. Get GitHub token
2. Create .env file
3. Install dependencies
4. Verify installation
5. Build database
6. Test search

Run this to get started: python quickstart.py
"""

import os
import sys
import subprocess
import platform

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_step(step_num, title):
    print(f"\n[STEP {step_num}] {title}")
    print("-" * 70)

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def main():
    clear_screen()
    
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║              🚀 RAG APPLICATION - QUICK START SETUP 🚀             ║
║                                                                    ║
║  This script will guide you through the complete setup process     ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
""")
    
    # Step 1: GitHub Token
    print_step(1, "GitHub Personal Access Token")
    print("""
You need a GitHub token to access the GitHub API.

1. Visit: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Select scope: "public_repo"
4. Copy the token (starts with "ghp_")

Enter your GitHub token (or press Enter to skip):
""")
    
    github_token = input("GitHub Token: ").strip()
    
    if not github_token:
        print_warning("GitHub token skipped - you'll need to add it to .env manually")
        github_token = "ghp_your_token_here"
    else:
        print_success("Token received!")
    
    # Step 2: Create .env file
    print_step(2, "Create .env Configuration File")
    
    env_content = f"""# RAG Application Configuration
GITHUB_TOKEN={github_token}
GITHUB_OWNER=fastapi
GITHUB_REPO=fastapi
LOG_LEVEL=INFO
"""
    
    # Create .env in appropriate location
    env_paths = [
        'backend/backend/.env',
        'backend/.env',
        '.env'
    ]
    
    env_file = None
    for path in env_paths:
        dir_path = os.path.dirname(path)
        if os.path.exists(dir_path) or dir_path == '':
            env_file = path
            break
    
    if env_file is None:
        env_file = 'backend/backend/.env'
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print_success(f"Created .env file at: {env_file}")
    except Exception as e:
        print_error(f"Failed to create .env: {e}")
        print_info("Create manually with the content above")
        return 1
    
    # Step 3: Check Python
    print_step(3, "Python Environment")
    
    version = sys.version_info
    print_success(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or version.minor < 8:
        print_error("Python 3.8+ required")
        return 1
    
    # Step 4: Create virtual environment
    print_step(4, "Python Virtual Environment")
    
    venv_path = "venv" if os.path.exists("venv") or \
                not os.path.exists("backend") else "backend/venv"
    
    if not os.path.exists(venv_path):
        print_info(f"Creating virtual environment in: {venv_path}")
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
            print_success("Virtual environment created")
        except Exception as e:
            print_error(f"Failed to create venv: {e}")
            return 1
    else:
        print_success("Virtual environment already exists")
    
    # Step 5: Install dependencies
    print_step(5, "Install Dependencies")
    
    req_file = None
    for path in ['backend/backend/requirements.txt', 'backend/requirements.txt', 'requirements.txt']:
        if os.path.exists(path):
            req_file = path
            break
    
    if not req_file:
        print_error("requirements.txt not found!")
        return 1
    
    if platform.system() == 'Windows':
        pip_cmd = [os.path.join(venv_path, 'Scripts', 'pip.exe')]
        python_cmd = [os.path.join(venv_path, 'Scripts', 'python.exe')]
        activate_cmd = os.path.join(venv_path, 'Scripts', 'Activate.ps1')
    else:
        pip_cmd = [os.path.join(venv_path, 'bin', 'pip')]
        python_cmd = [os.path.join(venv_path, 'bin', 'python')]
        activate_cmd = os.path.join(venv_path, 'bin', 'activate')
    
    print_info(f"Installing packages from {req_file}...")
    try:
        subprocess.run(pip_cmd + ["install", "-r", req_file], check=True)
        print_success("Dependencies installed")
    except Exception as e:
        print_error(f"Installation failed: {e}")
        return 1
    
    # Step 6: Test installation
    print_step(6, "Verify Installation")
    
    print_info("Checking modules...")
    modules = ['chromadb', 'sentence_transformers', 'fastapi', 'requests']
    
    for module in modules:
        try:
            __import__(module)
            print_success(f"{module} installed")
        except ImportError:
            print_error(f"{module} not found")
            return 1
    
    # Step 7: Build database
    print_step(7, "Download & Build Embeddings Database")
    
    print("""
This step will:
1. Download Python files from FastAPI GitHub repo
2. Extract functions and classes
3. Generate semantic embeddings
4. Store in vector database

⏱️  First run takes 10-30 minutes (subsequent runs are instant)
""")
    
    response = input("Ready to build? (yes/no): ").strip().lower()
    
    if response == 'yes':
        try:
            result = subprocess.run(
                python_cmd + ["-m", "main"],
                capture_output=False
            )
            if result.returncode == 0:
                print_success("Database build completed!")
            else:
                print_warning("Database build may have issues")
        except Exception as e:
            print_error(f"Failed to build database: {e}")
            print_info("You can run 'python main.py --build' later")
    else:
        print_info("Skipping database build for now")
        print_info("Run 'python main.py --build' when ready")
    
    # Summary
    print_header("✅ Setup Complete!")
    
    print(f"""
Activation command (run this in new terminal):
  
  Windows:  {venv_path}\\Scripts\\Activate.ps1
  Mac/Linux: source {venv_path}/bin/activate

Next steps:

1. Activate environment:
   Windows:  .\\{venv_path}\\Scripts\\Activate.ps1
   Mac/Linux: source {venv_path}/bin/activate

2. Run application:
   python -m main              # Interactive mode
   python -m main --search     # Search only
   python -m main --stats      # Show statistics

3. Or start REST API:
   uvicorn api:app --reload

4. Read README.md for full documentation

Your GitHub token: {'✅ Set' if github_token != 'ghp_your_token_here' else '❌ Not set'}
Virtual environment: {venv_path}
Configuration file: {env_file}
""")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
