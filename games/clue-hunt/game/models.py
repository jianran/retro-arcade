"""
Clue Hunt — player model and game state persistence.
"""

import json
import os
from dataclasses import dataclass, field
from typing import Optional

SAVE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "savegame.json")


@dataclass
class Player:
    name: str
    family: str
    health: float = 10
    max_health: int = 10
    points: int = 0
    inventory: list = field(default_factory=list)
    solved_locations: list = field(default_factory=list)  # list of loc ids solved
    solved_count: int = 0  # number of clues solved
    current_location_index: int = 0  # 0-99, which clue the player is on
    location_progress: dict = field(default_factory=dict)  # loc_id -> stage_index
    cyber_hints_used: list = field(default_factory=list)  # loc indices where cyber hint was used
    encyclopedia_hints_used: list = field(default_factory=list)  # loc indices where lore hint was used
    wrong_answers: int = 0  # wrong answer count for current location
    is_poisoned: bool = False
    shield_uses: int = 0
    has_armor: bool = False
    notes: list = field(default_factory=list)
    combat_log: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "family": self.family,
            "health": self.health,
            "max_health": self.max_health,
            "points": self.points,
            "inventory": self.inventory,
            "solved_locations": self.solved_locations,
            "solved_count": self.solved_count,
            "current_location_index": self.current_location_index,
            "location_progress": self.location_progress,
            "cyber_hints_used": self.cyber_hints_used,
            "encyclopedia_hints_used": self.encyclopedia_hints_used,
            "wrong_answers": self.wrong_answers,
            "is_poisoned": self.is_poisoned,
            "shield_uses": self.shield_uses,
            "has_armor": self.has_armor,
            "notes": self.notes,
            "combat_log": self.combat_log,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Player":
        return cls(
            name=d["name"],
            family=d["family"],
            health=d.get("health", 10),
            max_health=d.get("max_health", 10),
            points=d.get("points", 0),
            inventory=d.get("inventory", []),
            solved_locations=d.get("solved_locations", []),
            solved_count=d.get("solved_count", 0),
            current_location_index=d.get("current_location_index", 0),
            location_progress=d.get("location_progress", {}),
            cyber_hints_used=d.get("cyber_hints_used", []),
            encyclopedia_hints_used=d.get("encyclopedia_hints_used", []),
            wrong_answers=d.get("wrong_answers", 0),
            is_poisoned=d.get("is_poisoned", False),
            shield_uses=d.get("shield_uses", 0),
            has_armor=d.get("has_armor", False),
            notes=d.get("notes", []),
            combat_log=d.get("combat_log", []),
        )

    def has_item(self, item_id: str) -> bool:
        return item_id in self.inventory

    def add_item(self, item_id: str):
        self.inventory.append(item_id)

    def remove_item(self, item_id: str):
        if item_id in self.inventory:
            self.inventory.remove(item_id)

    def can_use_cyber_hint(self, loc_index: int) -> bool:
        return self.family == "cyber" and loc_index not in self.cyber_hints_used

    def can_use_encyclopedia_hint(self, loc_index: int) -> bool:
        return self.family == "encyclopedia" and loc_index not in self.encyclopedia_hints_used

    def mark_cyber_hint_used(self, loc_index: int):
        if loc_index not in self.cyber_hints_used:
            self.cyber_hints_used.append(loc_index)

    def mark_encyclopedia_hint_used(self, loc_index: int):
        if loc_index not in self.encyclopedia_hints_used:
            self.encyclopedia_hints_used.append(loc_index)

    def take_damage(self, amount: float) -> float:
        """Apply damage, return amount blocked by defenses."""
        original = amount
        if self.has_armor:
            amount = max(0, amount - 1)
        if self.shield_uses > 0 and amount > 0:
            blocked = min(2, amount)
            amount -= blocked
            self.shield_uses -= 1
            if self.shield_uses <= 0 and "shield" in self.inventory:
                self.inventory.remove("shield")
        self.health = round(max(0, self.health - amount), 1)
        return original - amount  # blocked amount

    def heal(self, amount: float):
        self.health = round(min(self.max_health, self.health + amount), 1)


@dataclass
class NPC:
    name: str
    family: str
    health: float = 10
    max_health: int = 10
    weapon_id: str = ""
    location_index: int = 0

    def to_dict(self) -> dict:
        return {
            "name": self.name, "family": self.family, "health": self.health,
            "max_health": self.max_health, "weapon_id": self.weapon_id,
            "location_index": self.location_index
        }

    @classmethod
    def from_dict(cls, d: dict) -> "NPC":
        return cls(name=d["name"], family=d["family"], health=d.get("health", 10),
                   max_health=d.get("max_health", 10), weapon_id=d.get("weapon_id", ""),
                   location_index=d.get("location_index", 0))


NPC_NAMES = {
    "python": ["Viper", "Cobra", "Mamba", "Asp"],
    "rally": ["Blaze", "Inferno", "Ember", "Scorch"],
    "cyber": ["Cipher", "Binary", "Pixel", "Matrix"],
    "encyclopedia": ["Sage", "Scholar", "Scribe", "Oracle"],
}


def generate_npcs():
    """Create 16 NPCs, 4 per family, with random weapons and locations."""
    import random
    # Import here to avoid circular import
    from .data import SHOP_ITEMS, LOCATIONS
    npcs = []
    for family in ["python", "rally", "cyber", "encyclopedia"]:
        weapons = [wid for wid, item in SHOP_ITEMS.items() if item.get("type") == "weapon"]
        max_hp = 20 if family == "rally" else 10
        for name in NPC_NAMES[family]:
            npcs.append(NPC(
                name=name, family=family, health=max_hp, max_health=max_hp,
                weapon_id=random.choice(weapons),
                location_index=random.randint(0, len(LOCATIONS) - 1)
            ))
    return npcs


class GameState:
    """Manages all players and persistence."""

    def __init__(self):
        self.players: dict[str, Player] = {}
        self.npcs: list[NPC] = []
        self._load()
        if not self.npcs:
            self.npcs = generate_npcs()
            self.save()

    def _load(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                for name, pd in data.get("players", {}).items():
                    self.players[name.lower()] = Player.from_dict(pd)
                self.npcs = [NPC.from_dict(nd) for nd in data.get("npcs", [])]
            except (json.JSONDecodeError, KeyError):
                self.players = {}

    def save(self):
        data = {
            "players": {name: p.to_dict() for name, p in self.players.items()},
            "npcs": [n.to_dict() for n in self.npcs]
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def get_player(self, name: str) -> Optional[Player]:
        return self.players.get(name.lower())

    def create_player(self, name: str, family: str) -> Player:
        max_hp = 20 if family == "rally" else 10
        player = Player(name=name, family=family, health=max_hp, max_health=max_hp)
        self.players[name.lower()] = player
        self.save()
        return player

    def player_exists(self, name: str) -> bool:
        return name.lower() in self.players

    def all_players(self) -> list[Player]:
        return list(self.players.values())

    def get_leaderboard(self) -> list[Player]:
        return sorted(self.players.values(), key=lambda p: p.points, reverse=True)

    def delete_player(self, name: str):
        key = name.lower()
        if key in self.players:
            del self.players[key]
            self.save()
