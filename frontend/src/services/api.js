/**
 * RAG API Service
 * Centralized API communication with health checks and proper error handling
 */

const API_BASE_URL = 'http://localhost:8000';
const DEFAULT_TIMEOUT = 300000; // 5 minutes for long operations

/**
 * Make API request with timeout and error handling
 */
async function apiRequest(endpoint, method = 'GET', body = null) {
  const url = `${API_BASE_URL}${endpoint}`;
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
    mode: 'cors',
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT);

  try {
    options.signal = controller.signal;
    const response = await fetch(url, options);
    clearTimeout(timeoutId);

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      const errorMessage = data?.detail || data?.error || response.statusText || 'Request failed';
      throw new Error(`${response.status}: ${errorMessage}`);
    }

    return data;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      throw new Error('Request timeout - backend may be processing or unreachable');
    }
    throw error;
  }
}

/**
 * Check API health and connectivity
 */
export async function checkHealth() {
  try {
    const response = await apiRequest('/health');
    return response;
  } catch (error) {
    throw new Error(`Backend unreachable at ${API_BASE_URL}: ${error.message}`);
  }
}

/**
 * Build database from GitHub repository
 */
export async function buildDatabase(owner, repo, forceRebuild = false) {
  try {
    return await apiRequest('/build', 'POST', {
      owner,
      repo,
      force_rebuild: forceRebuild,
    });
  } catch (error) {
    throw new Error(`Failed to build database: ${error.message}`);
  }
}

/**
 * Search for code using semantic similarity
 */
export async function searchCode(query, nResults = 5) {
  try {
    return await apiRequest('/search', 'POST', {
      query,
      n_results: nResults,
    });
  } catch (error) {
    throw new Error(`Search failed: ${error.message}`);
  }
}

/**
 * Get database statistics
 */
export async function getStats() {
  try {
    return await apiRequest('/stats');
  } catch (error) {
    throw new Error(`Failed to get stats: ${error.message}`);
  }
}

export { API_BASE_URL };
