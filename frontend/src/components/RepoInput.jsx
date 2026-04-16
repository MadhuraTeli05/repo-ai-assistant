import { useState } from 'react';
import { buildDatabase } from '../services/api';
import './RepoInput.css';

export default function RepoInput({ onDatabaseReady, onError }) {
  const [owner, setOwner] = useState('');
  const [repo, setRepo] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [forceRebuild, setForceRebuild] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!owner.trim() || !repo.trim()) {
      onError('Please enter both repository owner and name');
      return;
    }

    setIsLoading(true);

    try {
      await buildDatabase(owner.trim(), repo.trim(), forceRebuild);
      onDatabaseReady();
    } catch (error) {
      onError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="repo-input">
      <div className="card">
        <h2>Load Repository</h2>
        <p className="card-subtitle">Enter a GitHub repository to process</p>
        
        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label htmlFor="owner">Owner</label>
            <input
              id="owner"
              type="text"
              value={owner}
              onChange={(e) => setOwner(e.target.value)}
              placeholder="e.g., 'facebook', 'python', etc."
              disabled={isLoading}
              maxLength="100"
            />
          </div>

          <div className="form-group">
            <label htmlFor="repo">Repository</label>
            <input
              id="repo"
              type="text"
              value={repo}
              onChange={(e) => setRepo(e.target.value)}
              placeholder="e.g., 'react', 'cpython', etc."
              disabled={isLoading}
              maxLength="100"
            />
          </div>

          <div className="form-group checkbox-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={forceRebuild}
                onChange={(e) => setForceRebuild(e.target.checked)}
                disabled={isLoading}
              />
              <span className="checkbox-text">Force rebuild (clear existing database)</span>
            </label>
          </div>

          <div className="form-actions">
            <button
              type="submit"
              disabled={isLoading}
              className="btn btn-primary btn-large"
            >
              {isLoading ? (
                <>
                  <span className="spinner"></span>
                  Processing...
                </>
              ) : (
                'Process Repository'
              )}
            </button>
          </div>
        </form>

        {isLoading && (
          <div className="processing-info">
            <p>This may take several minutes depending on repository size...</p>
          </div>
        )}
      </div>
    </div>
  );
}
