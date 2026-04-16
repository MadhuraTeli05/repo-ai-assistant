import { useState } from 'react';
import { searchCode } from '../services/api';
import './SearchInput.css';

export default function SearchInput({ disabled, onResults, onError, chatHistory = [] }) {
  const [query, setQuery] = useState('');
  const [nResults, setNResults] = useState(5);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();

    if (!query.trim()) {
      onError('Please enter a search query');
      return;
    }

    setIsLoading(true);

    try {
      const trimmedQuery = query.trim();
      const results = await searchCode(trimmedQuery, nResults, chatHistory);

      if (onResults) {
        onResults(results, trimmedQuery);
      }

      setQuery('');
    } catch (error) {
      onError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="search-input">
      <div className="card">
        <h2>Search Code</h2>
        <p className="card-subtitle">Find relevant code using natural language</p>

        <form onSubmit={handleSearch} className="form">
          <div className="form-group">
            <label htmlFor="query">Query</label>
            <input
              id="query"
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Describe what you're looking for..."
              disabled={disabled || isLoading}
              maxLength="200"
            />
          </div>

          <div className="form-group">
            <label htmlFor="nResults">Results to show</label>
            <div className="slider-container">
              <input
                id="nResults"
                type="range"
                min="1"
                max="20"
                value={nResults}
                onChange={(e) => setNResults(parseInt(e.target.value))}
                disabled={disabled || isLoading}
                className="slider"
              />
              <span className="result-count">{nResults}</span>
            </div>
          </div>

          <button
            type="submit"
            disabled={disabled || isLoading}
            className="btn btn-primary btn-large"
          >
            {isLoading ? (
              <>
                <span className="spinner"></span>
                Searching...
              </>
            ) : (
              'Run Search'
            )}
          </button>
        </form>

        {disabled && !isLoading && (
          <div className="disabled-message">
            <p>Load a repository first to start searching</p>
          </div>
        )}
      </div>
    </div>
  );
}