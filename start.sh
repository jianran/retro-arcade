#!/bin/bash
# Retro Arcade — serve the hub and all games over HTTP
# Usage: bash start.sh [port]   (default port: 8137)
cd "$(dirname "$0")"
PORT="${1:-8137}"
echo "Retro Arcade → http://127.0.0.1:$PORT/"
open "http://127.0.0.1:$PORT/" 2>/dev/null || true
python3 -m http.server "$PORT"
