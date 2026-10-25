#!/bin/bash
# Clue Hunt - Start server + public tunnel
# One command to make the game accessible from any WiFi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Clue Hunt ==="
echo ""

# 1. Start the HTTP server (if not already running)
if lsof -i :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "[OK] Server already running on port 8080"
else
    echo "[...] Starting server on port 8080"
    python3 -m http.server 8080 &
    sleep 1
    echo "[OK] Server running"
fi

# 2. Start cloudflared tunnel
echo "[...] Starting Cloudflare tunnel"
cloudflared tunnel --url http://localhost:8080 2>&1 | while read line; do
    echo "$line"
    if echo "$line" | grep -q 'trycloudflare\.com'; then
        TUNNEL_URL=$(echo "$line" | grep -o 'https://[a-z0-9.-]*\.trycloudflare\.com')
        FULL_URL="${TUNNEL_URL}/clue_hunt.html"
        echo ""
        echo "============================================"
        echo "  GAME URL: $FULL_URL"
        echo "============================================"
        echo ""

        # Generate QR code
        python3 -c "
import qrcode
url = '$FULL_URL'
img = qrcode.make(url)
img.save('$SCRIPT_DIR/clue_hunt_qr.png')
print('QR code saved -> clue_hunt_qr.png')
" 2>/dev/null
    fi
done
