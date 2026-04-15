import { useState } from 'react';
import './ResultsDisplay.css';

export default function ResultsDisplay({ results }) {
  const [copiedId, setCopiedId] = useState(null);

  if (!results || !results.matches || results.matches.length === 0) {
    return (
      <div className="card empty-results">
        <div className="empty-content">
          <div className="empty-icon">📭</div>
          <h3>No results found</h3>
          <p>Try a different search query</p>
        </div>
      </div>
    );
  }

  const handleCopyCode = (code, id) => {
    navigator.clipboard.writeText(code);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const getSimilarityColor = (similarity) => {
    if (similarity >= 0.85) return '#10b981'; // Green
    if (similarity >= 0.7) return '#3b82f6';  // Blue
    if (similarity >= 0.5) return '#f59e0b'; // Amber
    return '#ef4444'; // Red
  };

  const formatCode = (code, maxLines = 20) => {
    const lines = code.split('\n');
    if (lines.length > maxLines) {
      return lines.slice(0, maxLines).join('\n') + '\n... (truncated)';
    }
    return code;
  };

  return (
    <div className="results-display">
      <div className="results-header">
        <h2>📋 Results</h2>
        <p className="results-info">
          Found <strong>{results.total_matches}</strong> match{results.total_matches !== 1 ? 'es' : ''}
        </p>
      </div>

      <div className="results-list">
        {results.matches.map((match, idx) => (
          <div key={match.id || idx} className="result-card">
            <div className="result-top">
              <div className="result-header">
                <div className="result-rank">#{idx + 1}</div>
                <div className="result-info">
                  <h3 className="result-name">{match.name}</h3>
                  <div className="result-meta">
                    <span className="badge badge-type">{match.type || 'code'}</span>
                    {match.file && (
                      <span className="result-file">📄 {match.file}</span>
                    )}
                  </div>
                </div>
              </div>

              {match.similarity !== undefined && (
                <div className="similarity">
                  <div className="similarity-bar">
                    <div
                      className="similarity-fill"
                      style={{
                        width: `${match.similarity * 100}%`,
                        backgroundColor: getSimilarityColor(match.similarity)
                      }}
                    ></div>
                  </div>
                  <div className="similarity-score">{Math.round(match.similarity * 100)}%</div>
                </div>
              )}
            </div>

            <div className="code-wrapper">
              <pre className="code-block"><code>{formatCode(match.code)}</code></pre>
              <button
                className="copy-btn"
                onClick={() => handleCopyCode(match.code, match.id)}
                title="Copy code"
              >
                {copiedId === match.id ? '✅ Copied!' : '📋 Copy'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
