import type { IndicatorDefinition, IndicatorSnapshot } from "./types";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ?? "http://127.0.0.1:8000";

async function requestJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`API request failed (${response.status}) for ${path}`);
  }
  return response.json() as Promise<T>;
}

export function fetchCatalog(): Promise<IndicatorDefinition[]> {
  return requestJson<IndicatorDefinition[]>("/api/catalog");
}

export function fetchIndicatorSnapshot(code: string): Promise<IndicatorSnapshot> {
  return requestJson<IndicatorSnapshot>(`/api/indicators/${encodeURIComponent(code)}`);
}
