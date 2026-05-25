#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$ROOT/.venv"
PYTHON="$VENV/bin/python"
DEV="${1:-}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3.11+ is required and was not found in PATH." >&2
  exit 1
fi

if [ ! -x "$PYTHON" ]; then
  python3 -m venv "$VENV"
fi

"$PYTHON" -m pip install --upgrade pip
if [ "$DEV" = "--dev" ]; then
  "$PYTHON" -m pip install -e "$ROOT[dev]"
else
  "$PYTHON" -m pip install -e "$ROOT"
fi

(cd "$ROOT/frontend" && npm install)

if [ ! -f "$ROOT/.env" ] && [ -f "$ROOT/env.example" ]; then
  cp "$ROOT/env.example" "$ROOT/.env"
fi

mkdir -p "$ROOT/data"
"$PYTHON" -m backend.cli init-db
