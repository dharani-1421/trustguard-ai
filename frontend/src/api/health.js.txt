/**
 * Health client. Uses Vite proxy (/api) unless VITE_API_BASE_URL is set.
 */
const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

export async function fetchHealth() {
  const response = await fetch(`${API_BASE}/api/health`, {
    method: "GET",
    headers: { Accept: "application/json" },
  });
  if (!response.ok) {
    throw new Error(`Health request failed (${response.status})`);
  }
  return response.json();
}
