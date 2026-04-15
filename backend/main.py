"""
RAG Application - CLI Entry Point

This script provides a command-line interface to:
1. Build embeddings database from a GitHub repository
2. Search the database with natural language queries
3. View database statistics

Usage:
    python main.py                # Interactive mode
    python main.py --build        # Build database only
    python main.py --search       # Search only
    python main.py --stats        # Show database stats
"""

import sys
import argparse
import logging
from rag_pipeline import get_pipeline
from config import DEFAULT_GITHUB_OWNER, DEFAULT_GITHUB_REPO, LOG_LEVEL
from vector_store import get_db_stats

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def print_separator():
    """Print a separator line."""
    print("-" * 70)


def interactive_mode():
    """Run in interactive mode - build and search."""
    pipeline = get_pipeline()
    
    print_header("🚀 RAG APPLICATION - Interactive Mode")
    
    # Step 1: Build database if needed
    print("\n📦 STEP 1: Initializing Database")
    print(f"   Repository: {DEFAULT_GITHUB_OWNER}/{DEFAULT_GITHUB_REPO}")
    
    success = pipeline.build_database(DEFAULT_GITHUB_OWNER, DEFAULT_GITHUB_REPO)
    if not success:
        logger.error("Failed to build database!")
        return
    
    # Step 2: Show database info
    print("\n📊 STEP 2: Database Statistics")
    pipeline.view_database()
    
    # Step 3: Interactive search
    print_header("STEP 3: Ask Questions")
    print("\n💡 Enter your questions to search for relevant code")
    print("📝 Type 'exit', 'quit', or 'q' to stop\n")
    
    while True:
        try:
            query = input("❓ Ask a question: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not query:
                print("⚠️  Please enter a question")
                continue
            
            # Search
            results = pipeline.search(query, n_results=5)
            
            # Display results
            print_separator()
            
            if not results['matches']:
                print("❌ No matching code found")
                print_separator()
                continue
            
            print(f"\n✅ Found {len(results['matches'])} relevant code chunks:\n")
            
            for match in results['matches']:
                print(f"#{match['rank']} - {match['name']} ({match['type']})")
                print(f"   📄 File: {match['file']}")
                
                if 'similarity' in match:
                    similarity_pct = int(match['similarity'] * 100)
                    print(f"   🎯 Relevance: {similarity_pct}%")
                
                # Show code snippet
                code = match['code']
                code_preview = code[:250].replace('\n', '\n   ')
                if len(code) > 250:
                    code_preview += "\n   ..."
                print(f"\n   💻 Code:\n   {code_preview}\n")
                print_separator()
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error during search: {e}")


def build_mode(owner: str = DEFAULT_GITHUB_OWNER, repo: str = DEFAULT_GITHUB_REPO):
    """Build database mode."""
    pipeline = get_pipeline()
    
    print_header(f"🔨 Building Database: {owner}/{repo}")
    
    success = pipeline.build_database(owner, repo, force_rebuild=False)
    
    if success:
        stats = pipeline.get_stats()
        print_separator()
        print("✅ Database build completed!")
        print(f"   📁 Files processed: {stats['files_processed']}")
        print(f"   📦 Chunks created: {stats['chunks_created']}")
        print(f"   💾 Embeddings stored: {stats['embeddings_stored']}")
        print(f"   ⚠️  Errors: {stats['errors']}")
        print_separator()
    else:
        print("❌ Failed to build database!")
        sys.exit(1)


def search_mode(query: str = None):
    """Search mode."""
    pipeline = get_pipeline()
    
    if not query:
        print_header("🔍 Search Mode")
        query = input("❓ Enter your question: ").strip()
    
    if not query:
        print("⚠️  No query provided")
        return
    
    print_separator()
    results = pipeline.search(query, n_results=5)
    
    if not results['matches']:
        print("❌ No results found")
        print_separator()
        return
    
    print(f"✅ Found {len(results['matches'])} matches:\n")
    
    for match in results['matches']:
        print(f"#{match['rank']} {match['name']} ({match['type']})")
        print(f"    📄 File: {match['file']}")
        if 'similarity' in match:
            print(f"    🎯 Relevance: {int(match['similarity']*100)}%")
        print(f"    💻 Code:\n{match['code'][:300]}...\n")
    
    print_separator()


def stats_mode():
    """Show database statistics."""
    print_header("📊 Database Statistics")
    
    stats = get_db_stats()
    
    print(f"\n📦 Total chunks: {stats['total_chunks']}")
    print(f"📁 Unique files: {stats['unique_files']}")
    
    if stats['files']:
        print("\n📚 Files indexed:")
        for file in sorted(stats['files'])[:10]:
            print(f"   - {file}")
        
        if len(stats['files']) > 10:
            print(f"   ... and {len(stats['files']) - 10} more")
    
    print()


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="🤖 RAG (Retrieval-Augmented Generation) Application",
        epilog="Examples:\n"
               "  python main.py                      # Interactive mode\n"
               "  python main.py --build              # Build database\n"
               "  python main.py --search 'question'  # Search\n"
               "  python main.py --stats              # Show stats\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--build',
        action='store_true',
        help='Build/rebuild the embeddings database'
    )
    
    parser.add_argument(
        '--rebuild',
        action='store_true',
        help='Force rebuild (clear and recreate database)'
    )
    
    parser.add_argument(
        '--search',
        nargs='?',
        const='',
        help='Search mode (optionally specify query)'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show database statistics'
    )
    
    parser.add_argument(
        '--owner',
        default=DEFAULT_GITHUB_OWNER,
        help=f'GitHub owner (default: {DEFAULT_GITHUB_OWNER})'
    )
    
    parser.add_argument(
        '--repo',
        default=DEFAULT_GITHUB_REPO,
        help=f'GitHub repo (default: {DEFAULT_GITHUB_REPO})'
    )
    
    args = parser.parse_args()
    
    try:
        if args.rebuild:
            pipeline = get_pipeline()
            logger.warning("🔄 Force rebuilding database...")
            from vector_store import delete_collection
            delete_collection()
            pipeline.build_database(args.owner, args.repo)
        
        elif args.build:
            build_mode(args.owner, args.repo)
        
        elif args.search is not None:
            search_mode(args.search if args.search else None)
        
        elif args.stats:
            stats_mode()
        
        else:
            # Default: interactive mode
            interactive_mode()
    
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()