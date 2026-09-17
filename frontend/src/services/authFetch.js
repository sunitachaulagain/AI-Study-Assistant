const API_BASE = "http://127.0.0.1:8000";

async function authFetch(path, options = {}) {
  const token = localStorage.getItem("access_token");

  const headers = {
    ...options.headers,
    Authorization: `Bearer ${token}`,
  };

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    localStorage.removeItem("access_token");
    window.location.reload();
    throw new Error("Session expired. Please log in again.");
  }

  return response;
}

export default authFetch;
