#!/usr/bin/env bash
set -euo pipefail

# Simple installer for local dev or users without Homebrew/AUR
# Usage examples:
#   ./scripts/install.sh            # prefer pipx
#   ./scripts/install.sh pip        # force pip install (user)
#   ./scripts/install.sh dev        # editable install (pipx if available)

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CMD=${1:-auto}

have_cmd() { command -v "$1" >/dev/null 2>&1; }

case "$CMD" in
  auto)
    if have_cmd pipx; then
      echo "Installing with pipx..."
      pipx install "$PROJECT_DIR"
    else
      echo "pipx not found. Installing with pip --user..."
      python3 -m pip install --user "$PROJECT_DIR"
      echo "Ensure ~/.local/bin is in your PATH."
    fi
    ;;
  pip)
    echo "Installing with pip --user..."
    python3 -m pip install --user "$PROJECT_DIR"
    echo "Ensure ~/.local/bin is in your PATH."
    ;;
  dev)
    if have_cmd pipx; then
      echo "Editable install with pipx..."
      pipx install --force --editable "$PROJECT_DIR"
    else
      echo "Editable install with pip --user..."
      python3 -m pip install --user -e "$PROJECT_DIR"
      echo "Ensure ~/.local/bin is in your PATH."
    fi
    ;;
  *)
    echo "Unknown option: $CMD"
    echo "Usage: $0 [auto|pip|dev]"
    exit 1
    ;;

esac

echo "Done. Run: hipodromo"
