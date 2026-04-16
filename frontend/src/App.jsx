import { useState, useEffect } from 'react';
import RepoInput from './components/RepoInput';
import SearchInput from './components/SearchInput';
import ResultsDisplay from './components/ResultsDisplay';
import { checkHealth } from './services/api';
import './App.css';

function App() {
  const [databaseReady, setDatabaseReady] = useState(false);
  const [searchResults, setSearchResults] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);   // 🔥 NEW
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [isAPIHealthy, setIsAPIHealthy] = useState(false);
  const [isCheckingAPI, setIsCheckingAPI] = useState(true);

  // Check API health
  useEffect(() => {
    const checkAPI = async () => {
      try {
        await checkHealth();
        setIsAPIHealthy(true);
      } catch (err) {
        console.error('API Health Check Failed:', err);
        setIsAPIHealthy(false);
      } finally {
        setIsCheckingAPI(false);
      }
    };
    checkAPI();
  }, []);

  // When repo loaded → reset chat
  const handleDatabaseReady = () => {
    setDatabaseReady(true);
    setSearchResults(null);
    setChatHistory([]);   // 🔥 RESET chat
    setError(null);
    setSuccess('✅ Database ready! You can now search.');
    setTimeout(() => setSuccess(null), 4000);
  };

  // 🔥 Updated search handler (adds memory)
  const handleSearchResults = (results, query) => {
    setSearchResults(results);
    setError(null);

    setChatHistory(prev => [
      ...prev.slice(-4),  // keep last 5 chats
      { question: query, answer: results.answer }
    ]);
  };

  const handleError = (errorMessage) => {
    let displayError = errorMessage;
    if (errorMessage.includes('unreachable')) {
      displayError = 'Cannot connect to backend at http://localhost:8000';
    } else if (errorMessage.includes('timeout')) {
      displayError = 'Backend request timed out. Processing may be in progress.';
    } else if (errorMessage.includes('500:')) {
      displayError =
        'Backend error: ' +
        (errorMessage.split('500:')[1]?.trim() || 'Internal server error');
    }
    setError(displayError);
    setSuccess(null);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="header-left">
            <p className="eyebrow">AI-Powered Repository Intelligence</p>
            <h1>RAG Code Search</h1>
            <p className="subtitle">
              Semantic search across GitHub codebases with retrieval-augmented answers
            </p>
          </div>

          <div className="header-status">
            <div className={`api-status ${isAPIHealthy ? 'healthy' : 'unhealthy'}`}>
              <span className="status-indicator"></span>
              {isCheckingAPI ? 'Checking...' : isAPIHealthy ? 'API Connected' : 'API Offline'}
            </div>
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="app-main">
        {!isCheckingAPI && !isAPIHealthy && (
          <div className="container">
            <div className="alert alert-error">
              <span className="alert-icon">⚠️</span>
              <div className="alert-content">
                <strong>Backend API Not Connected</strong>
                <p>Make sure the backend is running on http://localhost:8000</p>
                <p className="alert-small">
                  Command: <code>uvicorn api:app --reload</code>
                </p>
              </div>
            </div>
          </div>
        )}

        <div className="container">
          {/* Error */}
          {error && (
            <div className="alert alert-error">
              <span className="alert-icon">❌</span>
              <div className="alert-content">
                <strong>Error</strong>
                <p>{error}</p>
              </div>
              <button className="alert-close" onClick={() => setError(null)}>✕</button>
            </div>
          )}

          {/* Success */}
          {success && (
            <div className="alert alert-success">
              <span className="alert-icon">✓</span>
              <div className="alert-content">{success}</div>
              <button className="alert-close" onClick={() => setSuccess(null)}>✕</button>
            </div>
          )}

          <div className="layout">
            {/* LEFT SIDE */}
            <div className="column left-column">
              <RepoInput
                onDatabaseReady={handleDatabaseReady}
                onError={handleError}
              />

              <SearchInput
                disabled={!databaseReady}
                onResults={handleSearchResults}
                onError={handleError}
                chatHistory={chatHistory}   // 🔥 PASS HISTORY
              />
            </div>

            {/* RIGHT SIDE */}
            <div className="column right-column">
              {databaseReady ? (
                searchResults ? (
                  <>
                    {/* 🔥 Chat history display */}
                    <div className="card">
                      <h3>💬 Conversation</h3>
                      {chatHistory.map((msg, idx) => (
                        <div key={idx} style={{ marginBottom: '12px' }}>
                          <p><b>You:</b> {msg.question}</p>
                          <p><b>AI:</b> {msg.answer}</p>
                          <hr />
                        </div>
                      ))}
                    </div>

                    <ResultsDisplay results={searchResults} />
                  </>
                ) : (
                  <div className="card empty-state">
                    <div className="empty-content">
                      <div className="empty-icon">⌁</div>
                      <h3>Search for Code</h3>
                      <p>Run a natural-language query to surface relevant snippets</p>
                    </div>
                  </div>
                )
              ) : (
                <div className="card placeholder">
                  <div className="placeholder-content">
                    <div className="placeholder-icon">◈</div>
                    <h3>Load a Repository First</h3>
                    <p>Build the vector index from a GitHub repository to begin search</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="container">
          <p>RAG Code Search • Powered by ChromaDB, Embeddings, and FastAPI</p>
        </div>
      </footer>
    </div>
  );
}

export default App;