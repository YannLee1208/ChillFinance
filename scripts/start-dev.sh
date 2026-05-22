#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$ROOT/.venv/bin/python"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"

if [ ! -x "$PYTHON" ]; then
  echo "Virtual environment not found. Run scripts/bootstrap.sh first." >&2
  exit 1
fi

cleanup() {
  if [ -n "${BACKEND_PID:-}" ]; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

(cd "$ROOT" && "$PYTHON" -m uvicorn backend.app:create_app --factory --host 127.0.0.1 --port "$BACKEND_PORT" --reload) &
BACKEND_PID=$!

echo "Backend:  http://127.0.0.1:$BACKEND_PORT"
echo "Frontend: http://127.0.0.1:$FRONTEND_PORT"

(cd "$ROOT/frontend" && VITE_API_BASE_URL="http://127.0.0.1:$BACKEND_PORT" npm run dev -- --host 127.0.0.1 --port "$FRONTEND_PORT")
