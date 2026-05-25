#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$ROOT/.venv/bin/python"
DOMAIN=""
CODES=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --domain)
      DOMAIN="${2:-}"
      shift 2
      ;;
    --codes)
      CODES="${2:-}"
      shift 2
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

if [ ! -x "$PYTHON" ]; then
  echo "Virtual environment not found. Run scripts/bootstrap.sh first." >&2
  exit 1
fi

"$PYTHON" -m backend.cli init-db
if [ -n "$CODES" ]; then
  "$PYTHON" -m backend.cli ingest --codes "$CODES"
elif [ -n "$DOMAIN" ]; then
  "$PYTHON" -m backend.cli ingest-domain "$DOMAIN"
else
  "$PYTHON" -m backend.cli ingest
fi
