#!/usr/bin/env python3
"""Clue Hunt — Multiplayer Game Server."""
import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

PORT = 8080
STATE_FILE = os.path.join(os.path.dirname(__file__), "shared_state.json")


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"players": {}, "npcs": [], "ultimateMaster": None, "clueMaster": None}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


class GameHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/game/save":
            self._handle_save()
        elif path == "/api/game/login":
            self._handle_login()
        else:
            self.send_error(404)
        return

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/game/load":
            self._handle_load()
        elif path == "/api/leaderboard":
            self._handle_leaderboard()
        elif path == "/api/ping":
            self._handle_ping()
        else:
            super().do_GET()

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length > 0:
            return json.loads(self.rfile.read(length))
        return {}

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _handle_save(self):
        try:
            data = self._read_body()
            state = load_state()
            # Merge player data — never downgrade
            if "player" in data and "name" in data["player"]:
                p = data["player"]
                key = p["name"].lower()
                if key not in state["players"]:
                    state["players"][key] = {}
                existing = state["players"][key]
                # For inventory, solved_locations, points, solved_count — keep whichever is better
                new_inv = p.get("inventory", [])
                old_inv = existing.get("inventory", [])
                if len(new_inv) >= len(old_inv):
                    existing["inventory"] = new_inv
                new_solved = p.get("solved_locations", [])
                old_solved = existing.get("solved_locations", [])
                if len(new_solved) >= len(old_solved):
                    existing["solved_locations"] = new_solved
                if p.get("points", 0) >= existing.get("points", 0):
                    existing["points"] = p["points"]
                if p.get("solved_count", 0) >= existing.get("solved_count", 0):
                    existing["solved_count"] = p["solved_count"]
                # Health and other fields — always update
                for field in ["health", "max_health", "family", "current_location_index",
                             "location_progress", "cyber_hints_used", "encyclopedia_hints_used",
                             "wrong_answers", "is_poisoned", "shield_uses", "has_armor",
                             "notes", "combat_log", "weapon_wrappers", "kill_streak",
                             "auto_mode", "artifacts", "achievements"]:
                    if field in p:
                        existing[field] = p[field]

            # Merge NPCs if provided
            if "npcs" in data:
                state["npcs"] = data["npcs"]

            # Merge master roles
            if "ultimateMaster" in data:
                state["ultimateMaster"] = data["ultimateMaster"]
            if "clueMaster" in data:
                state["clueMaster"] = data["clueMaster"]

            save_state(state)
            self._send_json({"ok": True, "playerCount": len(state["players"])})
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 400)

    def _handle_login(self):
        try:
            data = self._read_body()
            name = data.get("name", "").strip()
            family = data.get("family", "")
            is_new = data.get("is_new", False)

            state = load_state()
            key = name.lower()

            if is_new:
                if key in state["players"]:
                    self._send_json({"ok": False, "error": f"Player '{name}' already exists."}, 409)
                    return
                state["players"][key] = {
                    "name": name,
                    "family": family,
                    "health": 20 if family == "rally" else 10,
                    "max_health": 20 if family == "rally" else 10,
                    "points": 0,
                    "inventory": [],
                    "solved_locations": [],
                    "solved_count": 0,
                    "current_location_index": 0,
                    "location_progress": {},
                    "cyber_hints_used": [],
                    "encyclopedia_hints_used": [],
                    "wrong_answers": 0,
                    "is_poisoned": False,
                    "shield_uses": 0,
                    "has_armor": False,
                    "notes": [],
                    "combat_log": [],
                    "weapon_wrappers": {},
                    "kill_streak": 0,
                    "artifacts": [],
                }
            else:
                if key not in state["players"]:
                    self._send_json({"ok": False, "error": f"Player '{name}' not found."}, 404)
                    return

            save_state(state)
            self._send_json({
                "ok": True,
                "player": state["players"][key],
                "npcs": state["npcs"],
                "ultimateMaster": state.get("ultimateMaster"),
                "clueMaster": state.get("clueMaster"),
            })
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 400)

    def _handle_load(self):
        try:
            state = load_state()
            # Accept optional ?player=Name to return just that player's data + shared state
            qs = urlparse(self.path).query
            player_name = None
            for param in qs.split("&"):
                if param.startswith("player="):
                    from urllib.parse import unquote
                    player_name = unquote(param[7:])
                    break

            result = {
                "npcs": state.get("npcs", []),
                "ultimateMaster": state.get("ultimateMaster"),
                "clueMaster": state.get("clueMaster"),
                "playerCount": len(state.get("players", {})),
            }
            if player_name:
                result["player"] = state.get("players", {}).get(player_name.lower())
            self._send_json(result)
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 400)

    def _handle_leaderboard(self):
        state = load_state()
        players = list(state.get("players", {}).values())
        players.sort(key=lambda p: p.get("points", 0), reverse=True)
        board = []
        for p in players[:20]:
            board.append({
                "name": p["name"],
                "family": p["family"],
                "points": p.get("points", 0),
                "solved_count": p.get("solved_count", 0),
                "health": p.get("health", 10),
            })
        self._send_json({"leaderboard": board, "totalPlayers": len(players)})

    def _handle_ping(self):
        state = load_state()
        self._send_json({
            "online": True,
            "players": len(state.get("players", {})),
            "hasUltimateMaster": bool(state.get("ultimateMaster")),
            "hasClueMaster": bool(state.get("clueMaster")),
        })

    def log_message(self, format, *args):
        path = urlparse(args[0] if args else "").path if args else ""
        if path.startswith("/api/"):
            sys.stderr.write("[API] %s - %s\n" % (self.address_string(), format % args))
        # suppress static file logs


def main():
    # Kill existing server on port 8080
    os.system("lsof -i :8080 -sTCP:LISTEN -t 2>/dev/null | xargs kill -9 2>/dev/null")
    import time
    time.sleep(0.5)

    server = HTTPServer(("0.0.0.0", PORT), GameHandler)
    print(f"\n  🏰 Clue Hunt Multiplayer Server")
    print(f"  📡 http://0.0.0.0:{PORT}")
    print(f"  Players: {len(load_state().get('players', {}))}")
    print(f"  Press Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
