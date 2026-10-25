"""
Clue Hunt — game engine: command processing, puzzle logic, combat, shop.
"""

import random
import sys
from .data import FAMILIES, LOCATIONS, SHOP_ITEMS
from .models import GameState, Player, NPC

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

FAMILY_COLORS = {
    "python": GREEN,
    "rally": RED,
    "cyber": CYAN,
    "encyclopedia": YELLOW,
}

FAMILY_EMBLEMS = {
    "python": "\U0001F40D",       # snake
    "rally": "\U0001F525",        # fire
    "cyber": "\U0001F4BB",        # laptop
    "encyclopedia": "\U0001F4DA", # books
}


def c(family: str) -> str:
    return FAMILY_COLORS.get(family, WHITE)


def emblem(family: str) -> str:
    return FAMILY_EMBLEMS.get(family, "")


def fmt_hp(hp: float) -> str:
    """Format HP: whole numbers as int, fractional as 1 decimal."""
    return f"{hp:g}"


class GameEngine:
    def __init__(self):
        self.state = GameState()
        self.player = None
        self.running = False

    # ── Status Bar ────────────────────────────────────────────────

    def _status_bar(self):
        if not self.player:
            return
        fam = FAMILIES[self.player.family]
        color = c(self.player.family)
        idx = self.player.current_location_index
        total = len(LOCATIONS)
        loc = LOCATIONS[idx] if idx < total else LOCATIONS[-1]
        hp_str = f"{fmt_hp(self.player.health)}/{self.player.max_health}"
        print(f"\n{BOLD}{color}HP: {hp_str} | Family Points: {self.player.points} | "
              f"Location: Clue {idx + 1}/{total} ({loc['name']}, {loc['city']}){RESET}")
        print(f"{DIM}{'─' * 70}{RESET}")

    # ── Entry Points ──────────────────────────────────────────────

    def run(self):
        self.running = True
        self._title_screen()
        while self.running:
            try:
                if self.player:
                    self._status_bar()
                cmd = input(f"{BOLD}> {RESET}").strip()
                if cmd:
                    self._dispatch(cmd)
            except KeyboardInterrupt:
                print(f"\n{YELLOW}Use 'quit' to exit safely.{RESET}")
            except EOFError:
                self._cmd_quit()

    def _title_screen(self):
        print(f"""
{RESET}
  {BOLD}{CYAN}╔══════════════════════════════════════════════════════════════╗
  ║                                                              ║
  ║   {YELLOW}█▀▀ █   █ █▀▀   {MAGENTA}█░█ █▀▀ █▀▀▀ ▀▀█▀▀   {CYAN}║
  ║   {YELLOW}█▄▄ █▄▄ █ █▀▀   {MAGENTA}█▀█ █▀▀ █ █░ ░█    {CYAN}║
  ║   {YELLOW}█▀  █▀▀ █ █▄▄   {MAGENTA}█▀█ █▄▄ █▄█░ ░█    {CYAN}║
  ║                                                              ║
  ║   {DIM}100 Clues. 4 Families. A Secret Global Race for History.{CYAN}  ║
  ║                                                              ║
  ╚══════════════════════════════════════════════════════════════╝{RESET}

  {RED}{BOLD}THE BRUTAL GLOBAL WAR{RESET}

  For centuries, four powerful families have waged a shadow war for
  control of the world's most dangerous secret: the {BOLD}Master Family Serum{RESET} —
  a legendary formula whose ingredients are hidden across 100 sacred
  sites around the globe. Each family seeks to collect all 100 clues,
  assemble the serum, and crown their bloodline supreme.

  These families are {RED}WORST ENEMIES{RESET}. They kill. They sabotage.
  They buy weapons — swords, bombs, poison — and they use them.

  {BOLD}The Four Families:{RESET}

    {GREEN}[Python]{RESET}  — {DIM}Masters of lethal inventory. Starts with one random weapon.{RESET}
    {RED}[Rally]{RESET}   — {DIM}High endurance. Starts with 20 Health Points instead of 10.{RESET}
    {CYAN}[Cyber]{RESET}   — {DIM}Tech geniuses. 1 free decryption hint per clue location.{RESET}
    {YELLOW}[Encyclopedia]{RESET} — {DIM}Infinite knowledge. 1 free lore hint per clue location.{RESET}

  {BOLD}GRAND FINALE:{RESET} Reach Clue 100 to unlock the secret of the Master Family
  Serum and crown your family as the supreme rulers of all four houses.

  Type {BOLD}'login <name>' or 'new <name>'{RESET} to begin.
  Type {BOLD}'help'{RESET} for all commands.
""")

    # ── Command Dispatch ──────────────────────────────────────────

    def _dispatch(self, raw: str):
        cmd = raw.strip().lower()

        # always-available commands
        if cmd == "help":
            self._cmd_help()
        elif cmd == "quit" or cmd == "exit":
            self._cmd_quit()
            return

        # login / new character
        if self.player is None:
            if cmd.startswith("login ") or cmd.startswith("new "):
                parts = raw.strip().split(None, 1)
                if len(parts) >= 2:
                    self._cmd_login(parts[1], is_new=cmd.startswith("new "))
            elif cmd == "leaderboard" or cmd == "lb":
                self._cmd_leaderboard()
            elif cmd == "families":
                self._cmd_families()
            else:
                print(f"{DIM}Please login first: 'login <name>' or 'new <name>'{RESET}")
            return

        # logged-in commands
        if cmd.startswith("attack ") or cmd.startswith("kill "):
            target = raw.strip().split(None, 1)[1] if " " in raw.strip() else ""
            self._cmd_attack(target)
        elif cmd == "shop" or cmd == "store":
            self._cmd_shop()
        elif cmd.startswith("buy "):
            item = raw.strip().split(None, 1)[1] if " " in raw.strip() else ""
            self._cmd_buy(item)
        elif cmd.startswith("use "):
            item = raw.strip().split(None, 1)[1] if " " in raw.strip() else ""
            self._cmd_use(item)
        elif cmd in ("inventory", "inv", "i"):
            self._cmd_inventory()
        elif cmd in ("status", "stats", "st"):
            self._cmd_status()
        elif cmd in ("locations", "places", "loc"):
            self._cmd_locations()
        elif cmd.startswith("go ") or cmd.startswith("travel "):
            dest = raw.strip().split(None, 1)[1] if " " in raw.strip() else ""
            self._cmd_travel(dest)
        elif cmd == "hint":
            self._cmd_hint()
        elif cmd == "decrypt":
            self._cmd_decrypt()
        elif cmd == "lore":
            self._cmd_lore()
        elif cmd in ("leaderboard", "lb"):
            self._cmd_leaderboard()
        elif cmd == "save":
            self.state.save()
            print(f"{GREEN}Game saved.{RESET}")
        elif cmd in ("notes", "journal"):
            self._cmd_notes()
        elif cmd in ("families", "family"):
            self._cmd_family_info()
        elif cmd in ("npcs", "npc"):
            self._cmd_npcs()
        elif cmd == "solve":
            self._cmd_solve_prompt()
        else:
            # treat as a puzzle action or answer attempt
            self._handle_puzzle_action(raw.strip())

    # ── Login ─────────────────────────────────────────────────────

    def _cmd_login(self, name: str, is_new: bool):
        name = name.strip().title()
        if not name:
            print(f"{RED}Please enter a valid name.{RESET}")
            return

        if is_new:
            if self.state.player_exists(name):
                print(f"{YELLOW}A player named '{name}' already exists. Use 'login {name}' instead.{RESET}")
                return
            self._create_character(name)
        else:
            player = self.state.get_player(name)
            if player:
                self.player = player
                self._show_welcome_back()
            else:
                print(f"{YELLOW}No player named '{name}' found. Use 'new {name}' to create one.{RESET}")

    def _create_character(self, name: str):
        print(f"\n{BOLD}Choose your family:{RESET}")
        print(f"  {GREEN}[P]ython{RESET}  — Masters of lethal inventory. Starts with one random weapon.")
        print(f"  {RED}[R]ally{RESET}   — High endurance. Starts with 20 HP instead of 10.")
        print(f"  {CYAN}[C]yber{RESET}   — Tech geniuses. 1 free decryption hint per location.")
        print(f"  {YELLOW}[E]ncyclopedia{RESET} — Infinite knowledge. 1 free historical lore hint per location.")

        while True:
            choice = input(f"\n{BOLD}Family [P/R/C/E]: {RESET}").strip().lower()
            if choice in ("p", "python"):
                family = "python"
                break
            elif choice in ("r", "rally"):
                family = "rally"
                break
            elif choice in ("c", "cyber"):
                family = "cyber"
                break
            elif choice in ("e", "encyclopedia"):
                family = "encyclopedia"
                break
            else:
                print(f"{RED}Invalid choice. Type P, R, C, or E.{RESET}")

        self.player = self.state.create_player(name, family)
        fam = FAMILIES[family]

        # Python family: start with one random weapon
        if family == "python":
            all_weapons = [wid for wid, item in SHOP_ITEMS.items() if item.get("type") == "weapon"]
            starter = random.choice(all_weapons)
            self.player.add_item(starter)
            w = SHOP_ITEMS[starter]
            print(f"\n{GREEN}[Python Bonus] You start with: {w['name']} ({w['damage']} dmg)!{RESET}")

        self.state.save()
        hp_str = f"{self.player.max_health} HP"
        if family == "rally":
            hp_str = f"{RED}20 HP{RESET}"
        print(f"\n{GREEN}Welcome, {c(family)}{name}{GREEN} of House {fam['name']}!{RESET}")
        print(f"{DIM}{fam['motto']}{RESET}")
        print(f"\n{BOLD}Family Trait:{RESET} {fam['trait']}")
        if family == "rally":
            print(f"{RED}You start with 20 HP — double the endurance of any rival!{RESET}")
        print(f"\n{DIM}Your first mission: Clue 1 of 100 at the Franklin Institute, Philadelphia.{RESET}")
        print(f"{DIM}Type 'help' to see all commands, or just start investigating.{RESET}")
        self._describe_current_location()

    def _show_welcome_back(self):
        fam = FAMILIES[self.player.family]
        print(f"\n{GREEN}Welcome back, {c(self.player.family)}{self.player.name}{GREEN} of House {fam['name']}.{RESET}")

        # show combat log
        if self.player.combat_log:
            print(f"\n{RED}While you were away:{RESET}")
            for msg in self.player.combat_log:
                print(f"  {RED}►{RESET} {msg}")
            self.player.combat_log.clear()
            self.state.save()

        # poison tick
        if self.player.is_poisoned:
            self.player.health = max(0, self.player.health - 1)
            print(f"\n{RED}The poison burns in your veins! -1 HP. ({fmt_hp(self.player.health)}/{self.player.max_health} HP){RESET}")
            if self.player.health <= 0:
                self._player_died("poison")
                return
            self.state.save()

        # show current location if mid-puzzle
        self._describe_current_location()
        self._check_npc_encounter()

    # ── NPC Encounters ────────────────────────────────────────────

    def _check_npc_encounter(self):
        """Check if rival NPCs are at the current location and auto-attack."""
        idx = self.player.current_location_index
        rivals = [n for n in self.state.npcs
                  if n.family != self.player.family
                  and n.location_index == idx
                  and n.health > 0]
        if not rivals:
            return
        attacker = random.choice(rivals)
        weapon = SHOP_ITEMS.get(attacker.weapon_id, {"name": "fists", "damage": 0.5, "reusable": True})
        dmg = weapon["damage"]
        blocked = self.player.take_damage(dmg)
        actual = dmg - blocked
        fam = FAMILIES[attacker.family]
        print(f"\n{RED}⚔ NPC AMBUSH! {fam['name']}'s {attacker.name} attacks you with {weapon['name']}!{RESET}")
        if blocked:
            print(f"{YELLOW}Your defenses blocked {fmt_hp(blocked)} damage!{RESET}")
        print(f"{RED}You take {fmt_hp(actual)} damage! ({fmt_hp(self.player.health)}/{self.player.max_health} HP){RESET}")
        if weapon.get("poisons"):
            self.player.is_poisoned = True
            print(f"{MAGENTA}You've been poisoned!{RESET}")
        if self.player.health <= 0:
            self._player_died(f"NPC {attacker.name} of House {fam['name']}")
        self.state.save()

    def _cmd_npcs(self):
        """List all 16 NPCs and their locations."""
        print(f"\n{BOLD}Active NPCs — 16 Rival Agents{RESET}\n")
        for family in ["python", "rally", "cyber", "encyclopedia"]:
            fam = FAMILIES[family]
            color = c(family)
            print(f"  {color}{fam['name']}{RESET} {emblem(family)}")
            for npc in self.state.npcs:
                if npc.family != family:
                    continue
                loc = LOCATIONS[npc.location_index] if npc.location_index < len(LOCATIONS) else {"name": "???"}
                weapon = SHOP_ITEMS.get(npc.weapon_id, {"name": "fists", "damage": 0.5})
                hp_str = f"{fmt_hp(npc.health)}/{npc.max_health} HP"
                alive = f"{GREEN}{hp_str}{RESET}" if npc.health > 0 else f"{RED}ELIMINATED{RESET}"
                print(f"    {BOLD}{npc.name}{RESET} — {alive} | {weapon['name']} ({weapon['damage']} dmg) | Clue {npc.location_index + 1} ({loc['name']})")
        print(f"\n{DIM}Attack NPCs with 'attack <name>'. They attack rival families on sight.{RESET}")

    # ── Puzzle Actions ────────────────────────────────────────────

    def _describe_current_location(self):
        idx = self.player.current_location_index
        if idx >= len(LOCATIONS):
            self._show_grand_finale()
            return
        loc = LOCATIONS[idx]

        if loc["id"] in self.player.solved_locations:
            return  # already solved, auto-advanced past

        progress = self.player.location_progress.get(loc["id"], 0)

        if progress == 0:
            print(loc["mystery"])
            stage = loc["stages"][0]
            print(f"\n{BOLD}Investigation — Stage 1/{len(loc['stages'])}{RESET}")
            print(stage["desc"])
        else:
            stage_idx = progress
            if stage_idx < len(loc["stages"]):
                stage = loc["stages"][stage_idx]
                print(f"\n{BOLD}Investigation — Stage {stage_idx + 1}/{len(loc['stages'])}{RESET}")
                print(stage["desc"])
            else:
                self._prompt_final_answer(loc)

    def _handle_puzzle_action(self, action: str):
        idx = self.player.current_location_index
        if idx >= len(LOCATIONS):
            return
        loc = LOCATIONS[idx]

        if loc["id"] in self.player.solved_locations:
            return  # shouldn't happen — auto-advance handles this

        progress = self.player.location_progress.get(loc["id"], 0)
        action_lower = action.lower().strip()

        # If all stages done, check for final answer
        if progress >= len(loc["stages"]):
            correct = loc["final_answer"].lower()
            if self._answer_matches(action_lower, correct):
                self.player.wrong_answers = 0  # reset for next location
                self._solve_location(loc)
            else:
                self.player.wrong_answers += 1
                w = self.player.wrong_answers
                close = self._close_match(action_lower, correct)
                print(f"\n{RED}That's not the answer. ({w} wrong attempt{'s' if w > 1 else ''}){RESET}")
                if close:
                    print(f"{YELLOW}You're close! Check your spelling.{RESET}")
                # Penalty after 2 wrong answers
                if w > 2:
                    penalty = w - 2  # 3rd wrong=-1, 4th wrong=-2, 5th wrong=-3...
                    self.player.points = max(0, self.player.points - penalty)
                    print(f"{RED}Penalty: -{penalty} point{'s' if penalty > 1 else ''}! (Total: {self.player.points}){RESET}")
                hint = loc.get("answer_hint", "")
                if hint:
                    print(f"{DIM}Hint: {hint}{RESET}")
                print(f"{DIM}Type the answer to solve this location, or 'hint' for help.{RESET}")
            self.state.save()
            return

        # Check against current stage triggers
        stage = loc["stages"][progress]

        if self._matches_trigger(action_lower, stage["triggers"]):
            print(f"\n{GREEN}{stage['success']}{RESET}")

            stage_points = 10
            self.player.points += stage_points
            print(f"{GREEN}+{stage_points} points! (Total: {self.player.points}){RESET}")

            if self.player.has_item("notepad"):
                self.player.notes.append(f"[{loc['name']}] {stage['success'][:100]}...")
                print(f"{DIM}[Notepad: clue recorded]{RESET}")

            self.player.location_progress[loc["id"]] = progress + 1
            self.state.save()

            new_progress = progress + 1
            if new_progress >= len(loc["stages"]):
                self._prompt_final_answer(loc)
            else:
                next_stage = loc["stages"][new_progress]
                print(f"\n{BOLD}Investigation — Stage {new_progress + 1}/{len(loc['stages'])}{RESET}")
                print(next_stage["desc"])
        else:
            print(f"\n{RED}That doesn't seem to help.{RESET}")
            print(f"{DIM}Hint: {stage['hint']}{RESET}")

    def _matches_trigger(self, action: str, triggers: list[str]) -> bool:
        """Fuzzy match action against trigger phrases. Requires investigation language."""
        STOP_WORDS = {"the", "a", "an", "to", "in", "at", "on", "for", "of", "and",
                      "or", "is", "it", "its", "this", "that", "with", "from", "by",
                      "around", "behind", "under", "over", "inside", "through", "up",
                      "down", "into", "onto", "me", "my", "i", "you", "your", "let"}
        INVESTIGATE_VERBS = {"examine", "search", "look", "check", "inspect", "read",
                             "open", "enter", "climb", "move", "lift", "pull", "push",
                             "find", "access", "study", "descend", "dig", "use", "spin",
                             "wade", "cross", "dive", "try", "approach", "touch", "slide",
                             "pry", "remove", "clean", "hold", "flip", "turn", "shake",
                             "knock", "peer", "reach", "feel", "tap", "press", "crawl",
                             "step", "walk", "run", "jump", "swim", "hack", "decode",
                             "translate", "solve", "answer", "say", "speak", "whisper",
                             "shout", "type", "input", "scan", "photograph", "sketch",
                             "investigate", "explore", "peek", "grab", "take", "get",
                             "watch", "observe", "note", "review", "probe", "test",
                             "pick", "sneak", "head", "go", "break", "smash", "force",
                             "cut", "pocket", "steal", "hide", "follow", "track"}
        action_lower = action.lower()
        for trigger in triggers:
            trigger_lower = trigger.lower()
            # Direct substring match
            if trigger_lower in action_lower or action_lower in trigger_lower:
                return True
            # Word overlap — requires at least one investigation verb in the action
            action_words = set(w for w in action_lower.split() if w not in STOP_WORDS)
            trigger_words = set(w for w in trigger_lower.split() if w not in STOP_WORDS)
            has_verb = bool(action_words & INVESTIGATE_VERBS)
            if not has_verb:
                continue
            # Content words only (exclude verbs) must overlap with trigger
            content_words = action_words - INVESTIGATE_VERBS
            overlap = len(content_words & trigger_words)
            if overlap >= 1:
                return True
        return False

    def _answer_matches(self, user_input: str, correct: str) -> bool:
        """Check if user input matches the correct answer, allowing extra words."""
        # Exact match
        if user_input == correct:
            return True
        # Answer appears as a word or substring in the input
        if correct in user_input:
            return True
        # Any word of the input matches the answer
        for word in user_input.split():
            if word == correct:
                return True
        return False

    def _close_match(self, user_input: str, correct: str) -> bool:
        """Check if any word in the input is within 1 character of the answer."""
        for word in user_input.split():
            if len(word) < 3:
                continue
            # Same length: check single character difference
            if len(word) == len(correct):
                diffs = sum(1 for a, b in zip(word, correct) if a != b)
                if diffs == 1:
                    return True
            # Off by one character
            if abs(len(word) - len(correct)) == 1:
                shorter = word if len(word) < len(correct) else correct
                longer = correct if len(word) < len(correct) else word
                # Check if removing one char from longer matches shorter
                for i in range(len(longer)):
                    if longer[:i] + longer[i+1:] == shorter:
                        return True
        return False

    def _prompt_final_answer(self, loc: dict):
        print(f"\n{BOLD}{YELLOW}All clues gathered! Now, what is the final answer?{RESET}")
        hint = loc.get("answer_hint", "")
        if hint:
            print(f"{DIM}Hint: {hint}{RESET}")
        print(f"{DIM}Type your answer to solve this location.{RESET}")

    def _cmd_solve_prompt(self):
        idx = self.player.current_location_index
        if idx >= len(LOCATIONS):
            return
        loc = LOCATIONS[idx]
        if loc["id"] not in self.player.solved_locations:
            progress = self.player.location_progress.get(loc["id"], 0)
            if progress >= len(loc["stages"]):
                self._prompt_final_answer(loc)
            else:
                print(f"{YELLOW}You haven't uncovered all the clues yet. Keep investigating!{RESET}")
                stage = loc["stages"][progress]
                print(f"{DIM}Current task: {stage['desc']}{RESET}")

    def _solve_location(self, loc: dict):
        print(f"\n{BOLD}{GREEN}Correct!{RESET}")
        print(f"{GREEN}The secret of {loc['name']} is yours!{RESET}")
        print(f"{GREEN}+{loc['points']} points! (Total: {self.player.points + loc['points']}){RESET}")

        self.player.points += loc["points"]
        self.player.solved_locations.append(loc["id"])
        self.player.solved_count += 1

        # Advance to next location
        self.player.current_location_index += 1
        self.state.save()

        # Check for Grand Finale
        if self.player.current_location_index >= len(LOCATIONS):
            self._show_grand_finale()
        else:
            next_loc = LOCATIONS[self.player.current_location_index]
            self.player.location_progress[next_loc["id"]] = 0
            print(f"\n{CYAN}Advancing to Clue {self.player.current_location_index + 1}: {next_loc['name']}, {next_loc['city']}...{RESET}")
            # Respawn eliminated NPCs at new random locations
            for npc in self.state.npcs:
                if npc.health <= 0:
                    npc.health = npc.max_health
                    npc.location_index = random.randint(0, len(LOCATIONS) - 1)
            self._describe_current_location()
            self._check_npc_encounter()

    # ── Travel (sequential only) ─────────────────────────────────

    def _cmd_travel(self, dest: str):
        # If destination isn't a recognized location, treat the whole phrase as exploration
        dest_lower = dest.lower().strip()
        for loc in LOCATIONS:
            if dest_lower in loc["name"].lower() or dest_lower in loc["id"].lower() or dest_lower in loc["city"].lower():
                print(f"{YELLOW}The race is sequential! You must solve Clue {self.player.current_location_index + 1} before moving on.{RESET}")
                print(f"{DIM}Focus on investigating your current location. Type 'locations' to see all 100 clues.{RESET}")
                return
        # Not a real location — treat the whole phrase as a puzzle action
        self._handle_puzzle_action(dest)

    def _cmd_hint(self):
        idx = self.player.current_location_index
        if idx >= len(LOCATIONS):
            return
        loc = LOCATIONS[idx]
        if not loc or loc["id"] in self.player.solved_locations:
            print(f"{YELLOW}No hint needed — this location is already solved.{RESET}")
            return
        progress = self.player.location_progress.get(loc["id"], 0)
        if progress >= len(loc["stages"]):
            hint = loc.get("answer_hint", "Think about the historical context of this place.")
            print(f"{YELLOW}Final answer hint: {hint}{RESET}")
        else:
            stage = loc["stages"][progress]
            print(f"{YELLOW}Hint: {stage['hint']}{RESET}")
            print(f"{DIM}You're on stage {progress + 1} of {len(loc['stages'])}.{RESET}")

    def _cmd_locations(self):
        total = len(LOCATIONS)
        solved = self.player.solved_count
        current_idx = self.player.current_location_index
        region = ""
        print(f"\n{BOLD}Global Progress — {solved}/{total} Clues Solved{RESET}\n")
        for i, loc in enumerate(LOCATIONS):
            # Show region headers
            new_region = loc.get("region", "")
            if new_region and new_region != region:
                region = new_region
                print(f"  {BOLD}{YELLOW}── {region} ──{RESET}")

            if loc["id"] in self.player.solved_locations:
                status = f"{GREEN}[#{i+1} SOLVED]{RESET}"
            elif i == current_idx:
                status = f"{CYAN}[#{i+1} ◄ HERE]{RESET}"
            elif i < current_idx:
                status = f"{DIM}[#{i+1} LOCKED]{RESET}"
            else:
                status = f"{DIM}[#{i+1} LOCKED]{RESET}"

            if i == current_idx or loc["id"] in self.player.solved_locations:
                print(f"    {status} {BOLD}{loc['name']}{RESET} — {loc['city']}")
            else:
                print(f"    {status} {DIM}{loc['name']} — {loc['city']}{RESET}")
        print(f"\n{DIM}The race is sequential. Solve each clue to unlock the next.{RESET}")

    # ── Cyber & Encyclopedia Family Commands ─────────────────────

    def _cmd_decrypt(self):
        if self.player.family != "cyber":
            print(f"{RED}Only the Cyber family can use decryption hints!{RESET}")
            return
        idx = self.player.current_location_index
        if idx >= len(LOCATIONS):
            return
        loc = LOCATIONS[idx]
        if not self.player.can_use_cyber_hint(idx):
            print(f"{YELLOW}You've already used your free decryption hint for this location.{RESET}")
            return
        self.player.mark_cyber_hint_used(idx)
        self.state.save()
        print(f"\n{CYAN}[Cyber Decryption] Running code-breaking algorithm...{RESET}")
        progress = self.player.location_progress.get(loc["id"], 0)
        if progress >= len(loc["stages"]):
            print(f"{CYAN}Decrypted answer hint: {loc.get('answer_hint', 'Unknown')}{RESET}")
        else:
            stage = loc["stages"][progress]
            print(f"{CYAN}Decrypted action: try '{stage['triggers'][0]}'{RESET}")
            print(f"{CYAN}Decrypted clue: {stage['hint']}{RESET}")
        print(f"{DIM}Your free hint for Clue {idx + 1} has been used.{RESET}")

    def _cmd_lore(self):
        if self.player.family != "encyclopedia":
            print(f"{RED}Only the Encyclopedia family can access historical lore!{RESET}")
            return
        idx = self.player.current_location_index
        if idx >= len(LOCATIONS):
            return
        loc = LOCATIONS[idx]
        if not self.player.can_use_encyclopedia_hint(idx):
            print(f"{YELLOW}You've already used your free lore hint for this location.{RESET}")
            return
        self.player.mark_encyclopedia_hint_used(idx)
        self.state.save()
        lore_text = loc.get("lore", "No additional lore available for this location.")
        print(f"\n{YELLOW}[Encyclopedia Archives] Historical Lore:{RESET}")
        print(f"{YELLOW}{lore_text}{RESET}")
        print(f"\n{DIM}Your free lore hint for Clue {idx + 1} has been used.{RESET}")

    # ── Shop ──────────────────────────────────────────────────────

    def _cmd_shop(self):
        print(f"\n{BOLD}The Underground Market{RESET}")
        print(f"{DIM}Your points: {self.player.points}{RESET}")

        # Tools
        print(f"\n  {BOLD}── Tools ──{RESET}")
        for item_id, item in SHOP_ITEMS.items():
            if item["type"] == "tool":
                owned = f"{GREEN}[OWNED]{RESET}" if self.player.has_item(item_id) else f"{DIM}[{item['price']} pts]{RESET}"
                print(f"    {owned} {BOLD}{item['name']}{RESET} — {item['description']}")

        # Weapons — tiered table format
        print(f"\n  {BOLD}── Weapon Catalog (20 Tiers) ──{RESET}")
        print(f"  {DIM}{'#':<3} {'Weapon':<22} {'Cost':<6} {'Dmg':<6} {'Type'}{RESET}")
        print(f"  {DIM}{'─' * 55}{RESET}")
        for item_id, item in SHOP_ITEMS.items():
            if item["type"] == "weapon":
                tier = item.get("tier", 0)
                name = item["name"]
                price = item["price"]
                dmg = item["damage"]
                reusable = "Reusable" if item.get("reusable") else "Single-use"
                owned_mark = f"{GREEN}*{RESET} " if self.player.has_item(item_id) else "  "
                dmg_str = f"{dmg}"
                if dmg == 10:
                    dmg_str = f"{RED}{dmg}{RESET}"
                print(f"  {owned_mark}{tier:<2} {BOLD}{name:<21}{RESET} {price:<5}pts {dmg_str:<7} {DIM}{reusable}{RESET}")
        print(f"  {DIM}{GREEN}* = owned{RESET}{DIM} | Red damage = instant kill at full HP{RESET}")

        # Defense
        print(f"\n  {BOLD}── Defense & Healing ──{RESET}")
        for item_id, item in SHOP_ITEMS.items():
            if item["type"] == "defense":
                owned = f"{GREEN}[OWNED]{RESET}" if self.player.has_item(item_id) else f"{DIM}[{item['price']} pts]{RESET}"
                print(f"    {owned} {BOLD}{item['name']}{RESET} — {item['description']}")

        print(f"\n{DIM}Type 'buy <item name>' to purchase (e.g. 'buy katana', 'buy mega bomb').{RESET}")

    def _cmd_buy(self, item_name: str):
        item_name_lower = item_name.lower().strip()
        # fuzzy match item
        matched = None
        for item_id, item in SHOP_ITEMS.items():
            if item_name_lower in item_id.lower() or item_name_lower in item["name"].lower():
                matched = (item_id, item)
                break

        if not matched:
            print(f"{RED}Item not found. Type 'shop' to see available items.{RESET}")
            return

        item_id, item = matched
        if self.player.has_item(item_id) and item.get("type") != "weapon":
            print(f"{YELLOW}You already own {item['name']}.{RESET}")
            return

        if self.player.points < item["price"]:
            print(f"{RED}Not enough points! {item['name']} costs {item['price']} pts. You have {self.player.points}.{RESET}")
            return

        self.player.points -= item["price"]
        self.player.add_item(item_id)

        # Handle special initialization
        if item_id == "shield":
            self.player.shield_uses = item.get("uses", 3)
        elif item_id == "armor":
            self.player.has_armor = True

        self.state.save()
        print(f"{GREEN}Purchased {item['name']} for {item['price']} pts!{RESET}")
        print(f"{DIM}Remaining points: {self.player.points}{RESET}")

    # ── Inventory & Items ─────────────────────────────────────────

    def _cmd_inventory(self):
        print(f"\n{BOLD}Inventory — {self.player.name} of House {FAMILIES[self.player.family]['name']}{RESET}")
        if not self.player.inventory:
            print(f"  {DIM}(empty){RESET}")
        else:
            for item_id in self.player.inventory:
                item = SHOP_ITEMS.get(item_id, {"name": item_id, "type": "unknown"})
                type_tag = f"[{item.get('type', 'item')}]"
                extra = ""
                if item_id == "shield":
                    extra = f" ({self.player.shield_uses} uses left)"
                elif item_id == "armor":
                    extra = " (active)"
                # Show damage for weapons
                dmg_str = ""
                if item.get("type") == "weapon":
                    dmg = item.get("damage", 0)
                    reusable = "reusable" if item.get("reusable") else "one-time"
                    dmg_str = f" {RED}{dmg} dmg{RESET} {DIM}({reusable}){RESET}"
                print(f"  {BOLD}{item['name']}{RESET} {DIM}{type_tag}{extra}{RESET}{dmg_str}")
        total_solved = len(self.player.solved_locations)
        print(f"\n{DIM}Points: {self.player.points} | Locations solved: {total_solved}/{len(LOCATIONS)}{RESET}")

    def _cmd_use(self, item_name: str):
        item_name_lower = item_name.lower().strip()
        matched = None
        for item_id, item in SHOP_ITEMS.items():
            if item_name_lower in item_id.lower() or item_name_lower in item["name"].lower():
                matched = (item_id, item)
                break

        if not matched:
            print(f"{RED}You don't have that item. Check 'inventory'.{RESET}")
            return

        item_id, item = matched
        if not self.player.has_item(item_id):
            print(f"{RED}You don't own {item['name']}.{RESET}")
            return

        # Use item effects
        if item_id == "flashlight":
            self.player.remove_item(item_id)
            loc = self._current_loc()
            print(f"{YELLOW}You flick on the flashlight. Its beam cuts through the darkness...{RESET}")
            if loc and loc["id"] not in self.player.solved_locations:
                progress = self.player.location_progress.get(loc["id"], 0)
                if progress < len(loc["stages"]):
                    stage = loc["stages"][progress]
                    print(f"{CYAN}The light reveals: {stage['hint']}{RESET}")
                else:
                    print(f"{CYAN}The light reveals: {loc.get('answer_hint', 'Think carefully...')}{RESET}")

        elif item_id == "magnifier":
            self.player.remove_item(item_id)
            loc = self._current_loc()
            print(f"{YELLOW}You study the area through the magnifying glass...{RESET}")
            if loc and loc["id"] not in self.player.solved_locations:
                progress = self.player.location_progress.get(loc["id"], 0)
                if progress < len(loc["stages"]):
                    stage = loc["stages"][progress]
                    print(f"{CYAN}Hidden detail: try '{random.choice(stage['triggers'])}'{RESET}")
                else:
                    print(f"{CYAN}Detail: {loc.get('answer_hint', '')}{RESET}")

        elif item_id == "compass":
            self.player.remove_item(item_id)
            unsolved = [l for l in LOCATIONS if l["id"] not in self.player.solved_locations and l["id"] != self.player.current_location]
            if unsolved:
                best = max(unsolved, key=lambda l: l["points"])
                print(f"{YELLOW}The compass needle spins and settles...{RESET}")
                print(f"{CYAN}It points toward: {best['name']}, {best['city']} ({best['points']} pts){RESET}")
            else:
                print(f"{YELLOW}The compass spins aimlessly. All locations solved!{RESET}")

        elif item_id == "lockpick":
            self.player.remove_item(item_id)
            loc = self._current_loc()
            if loc and loc["id"] not in self.player.solved_locations:
                progress = self.player.location_progress.get(loc["id"], 0)
                if progress < len(loc["stages"]):
                    stage = loc["stages"][progress]
                    # Auto-advance
                    print(f"{YELLOW}You deftly pick the lock, bypassing the obstacle...{RESET}")
                    print(f"{GREEN}{stage['success']}{RESET}")
                    self.player.points += 10
                    self.player.location_progress[loc["id"]] = progress + 1
                    self.state.save()
                    new_p = progress + 1
                    if new_p >= len(loc["stages"]):
                        self._prompt_final_answer(loc)
                    else:
                        ns = loc["stages"][new_p]
                        print(f"\n{BOLD}Stage {new_p + 1}/{len(loc['stages'])}{RESET}")
                        print(ns["desc"])
                else:
                    print(f"{YELLOW}Nothing left to pick — you're at the final answer stage.{RESET}")

        elif item_id == "health_potion":
            self.player.remove_item(item_id)
            heal = item.get("heal", 3)
            old_hp = self.player.health
            self.player.heal(heal)
            actual = self.player.health - old_hp
            print(f"{GREEN}You drink the health potion. +{fmt_hp(actual)} HP! ({fmt_hp(self.player.health)}/{self.player.max_health} HP){RESET}")

        elif item_id == "antidote":
            self.player.remove_item(item_id)
            if self.player.is_poisoned:
                self.player.is_poisoned = False
                print(f"{GREEN}The antidote neutralizes the poison in your system!{RESET}")
            heal = item.get("heal", 0)
            if heal:
                old_hp = self.player.health
                self.player.heal(heal)
                actual = self.player.health - old_hp
                if actual > 0:
                    print(f"{GREEN}+{fmt_hp(actual)} HP! ({fmt_hp(self.player.health)}/{self.player.max_health} HP){RESET}")

        elif item_id == "granite":
            self.player.remove_item(item_id)
            loc = self._current_loc()
            print(f"{YELLOW}You hurl the granite chunk. The noise echoes...{RESET}")
            if loc and loc["id"] not in self.player.solved_locations:
                progress = self.player.location_progress.get(loc["id"], 0)
                if progress < len(loc["stages"]):
                    stage = loc["stages"][progress]
                    print(f"{CYAN}The distraction reveals: {stage['hint']}{RESET}")

        else:
            print(f"{YELLOW}{item['name']} can't be 'used' directly — it's equipped or passive.{RESET}")

        self.state.save()

    def _cmd_notes(self):
        if not self.player.has_item("notepad"):
            print(f"{YELLOW}You need a Pen & Notepad to take notes. Buy one at the shop!{RESET}")
            return
        if not self.player.notes:
            print(f"{DIM}Your notepad is empty. Solve some clues first!{RESET}")
            return
        print(f"\n{BOLD}Your Notepad:{RESET}")
        for i, note in enumerate(self.player.notes, 1):
            print(f"  {i}. {note}")

    # ── Combat ────────────────────────────────────────────────────

    def _cmd_attack(self, target_name: str):
        if not target_name:
            print(f"{RED}Usage: attack <player name>{RESET}")
            return

        target = self.state.get_player(target_name)

        # Check if it's an NPC
        npc_target = None
        if not target:
            for n in self.state.npcs:
                if n.name.lower() == target_name.lower():
                    npc_target = n
                    break

        if npc_target:
            self._attack_npc(npc_target)
            return

        if not target:
            print(f"{RED}No player or NPC named '{target_name}' found.{RESET}")
            return

        if target.name.lower() == self.player.name.lower():
            print(f"{RED}You can't attack yourself!{RESET}")
            return

        if target.family == self.player.family:
            print(f"{RED}!!SAME FAMILY!!{RESET}")
            return

        if target.health <= 0:
            print(f"{YELLOW}{target.name} is already eliminated.{RESET}")
            return

        if self.player.health <= 0:
            print(f"{RED}You are eliminated! You cannot attack. Wait for respawn or create a new character.{RESET}")
            return

        # Find weapons in inventory
        weapons = [i for i in self.player.inventory if SHOP_ITEMS.get(i, {}).get("type") == "weapon"]
        if not weapons:
            print(f"{RED}You have no weapons! Buy one at the shop first.{RESET}")
            return

        print(f"\n{BOLD}{RED}Combat: {self.player.name} vs {target.name}{RESET}")
        print(f"{DIM}Your weapons:{RESET}")
        for i, w_id in enumerate(weapons, 1):
            w = SHOP_ITEMS[w_id]
            print(f"  {i}. {w['name']} — {w['damage']} dmg {'(reusable)' if w.get('reusable') else '(single use)'}")

        # Choose weapon
        if len(weapons) == 1:
            choice = 1
        else:
            try:
                choice = int(input(f"{BOLD}Choose weapon [1-{len(weapons)}]: {RESET}").strip())
            except ValueError:
                print(f"{RED}Invalid choice.{RESET}")
                return

        if choice < 1 or choice > len(weapons):
            print(f"{RED}Invalid weapon choice.{RESET}")
            return

        weapon_id = weapons[choice - 1]
        weapon = SHOP_ITEMS[weapon_id]
        base_damage = weapon["damage"]

        # Apply damage
        blocked = target.take_damage(base_damage)
        actual_damage = base_damage - blocked

        print(f"\n{RED}You attack {target.name} with {weapon['name']}!{RESET}")
        if blocked > 0:
            print(f"{YELLOW}{target.name}'s defenses blocked {blocked} damage!{RESET}")
        print(f"{RED}{target.name} takes {fmt_hp(actual_damage)} damage! ({fmt_hp(target.health)}/{target.max_health} HP){RESET}")

        # Handle poison
        if weapon.get("poisons"):
            target.is_poisoned = True
            print(f"{MAGENTA}{target.name} is now poisoned! They will lose 1 HP per turn.{RESET}")

        # Remove single-use weapon
        if not weapon.get("reusable", False):
            self.player.remove_item(weapon_id)
            print(f"{DIM}Your {weapon['name']} is spent.{RESET}")

        # Check elimination
        if target.health <= 0:
            print(f"\n{BOLD}{RED}{target.name} has been eliminated!{RESET}")
            bounty = 25
            self.player.points += bounty
            print(f"{GREEN}You collect a {bounty} pt bounty!{RESET}")
            # Notify target
            target.combat_log.append(
                f"You were eliminated by {self.player.name} of House {FAMILIES[self.player.family]['name']}! "
                f"Your health will reset to full when you next log in."
            )
            # Reset target
            target.health = target.max_health
            target.is_poisoned = False
            target.points = max(0, target.points - 20)
        else:
            target.combat_log.append(
                f"{self.player.name} of House {FAMILIES[self.player.family]['name']} attacked you "
                f"with {weapon['name']} for {fmt_hp(actual_damage)} damage! ({fmt_hp(target.health)}/{target.max_health} HP)"
            )

        self.state.save()

    def _attack_npc(self, npc):
        """Attack an NPC rival."""
        if npc.family == self.player.family:
            print(f"{RED}!!SAME FAMILY!!{RESET}")
            return
        weapons = [i for i in self.player.inventory if SHOP_ITEMS.get(i, {}).get("type") == "weapon"]
        if not weapons:
            print(f"{RED}You have no weapons! Buy one at the shop first.{RESET}")
            return

        print(f"\n{BOLD}{RED}Combat: {self.player.name} vs NPC {npc.name} ({FAMILIES[npc.family]['name']}){RESET}")
        if len(weapons) == 1:
            choice = 1
        else:
            print(f"{DIM}Your weapons:{RESET}")
            for i, w_id in enumerate(weapons, 1):
                w = SHOP_ITEMS[w_id]
                print(f"  {i}. {w['name']} — {w['damage']} dmg")
            try:
                choice = int(input(f"{BOLD}Choose weapon [1-{len(weapons)}]: {RESET}").strip())
            except ValueError:
                print(f"{RED}Invalid choice.{RESET}")
                return
        if choice < 1 or choice > len(weapons):
            return
        weapon_id = weapons[choice - 1]
        weapon = SHOP_ITEMS[weapon_id]
        dmg = weapon["damage"]
        npc.health = round(max(0, npc.health - dmg), 1)
        print(f"\n{RED}You attack {npc.name} with {weapon['name']}!{RESET}")
        print(f"{RED}{npc.name} takes {fmt_hp(dmg)} damage! ({fmt_hp(npc.health)}/{npc.max_health} HP){RESET}")
        if not weapon.get("reusable", False):
            self.player.remove_item(weapon_id)
            print(f"{DIM}{weapon['name']} spent.{RESET}")
        if npc.health <= 0:
            print(f"\n{BOLD}{RED}{npc.name} of House {FAMILIES[npc.family]['name']} eliminated!{RESET}")
            self.player.points += 15
            print(f"{GREEN}+15 pt NPC bounty! (Total: {self.player.points}){RESET}")
            npc.health = npc.max_health
            npc.location_index = random.randint(0, len(LOCATIONS) - 1)
            print(f"{DIM}{npc.name} respawns at a new location.{RESET}")
        self.state.save()

    def _player_died(self, cause: str):
        print(f"\n{BOLD}{RED}You have been eliminated by {cause}!{RESET}")
        print(f"{YELLOW}Your health resets to full. You lose 20 points.{RESET}")
        self.player.health = self.player.max_health
        self.player.is_poisoned = False
        self.player.points = max(0, self.player.points - 20)
        self.state.save()

    # ── Status & Info ─────────────────────────────────────────────

    def _cmd_status(self):
        fam = FAMILIES[self.player.family]
        color = c(self.player.family)
        idx = self.player.current_location_index
        total = len(LOCATIONS)
        loc_name = LOCATIONS[idx]["name"] if idx < total else "GRAND FINALE"
        loc_city = LOCATIONS[idx]["city"] if idx < total else "Antarctica"

        print(f"\n{BOLD}Status — {color}{self.player.name}{RESET} {emblem(self.player.family)}")
        print(f"  {BOLD}House:{RESET} {color}{fam['name']}{RESET} — {fam['motto']}")
        hp_color = GREEN if self.player.health > self.player.max_health / 2 else YELLOW if self.player.health > 2 else RED
        poison_tag = f" {MAGENTA}[POISONED]{RESET}" if self.player.is_poisoned else ""
        armor_tag = f" {CYAN}[ARMORED]{RESET}" if self.player.has_armor else ""
        print(f"  {BOLD}HP:{RESET} {hp_color}{fmt_hp(self.player.health)}/{self.player.max_health}{RESET}{poison_tag}{armor_tag}")
        print(f"  {BOLD}Family Points:{RESET} {self.player.points}")
        print(f"  {BOLD}Location:{RESET} Clue {idx + 1}/{total} — {loc_name}, {loc_city}")
        print(f"  {BOLD}Progress:{RESET} {self.player.solved_count}/{total} clues solved")
        print(f"  {BOLD}Inventory:{RESET} {len(self.player.inventory)} items (type 'inventory')")
        print(f"  {BOLD}Trait:{RESET} {fam['trait']}")
        if self.player.family == "cyber":
            used = len(self.player.cyber_hints_used)
            print(f"  {BOLD}Decrypt Hints:{RESET} {used} used (1 free per location)")
        elif self.player.family == "encyclopedia":
            used = len(self.player.encyclopedia_hints_used)
            print(f"  {BOLD}Lore Hints:{RESET} {used} used (1 free per location)")

    def _cmd_leaderboard(self):
        board = self.state.get_leaderboard()
        print(f"\n{BOLD}{YELLOW}Global Leaderboard{RESET}\n")
        if not board:
            print(f"  {DIM}No players yet. Create one with 'new <name>'!{RESET}")
            return
        medals = ["\U0001F947", "\U0001F948", "\U0001F949"]
        for i, p in enumerate(board):
            medal = medals[i] if i < 3 else f"  {i+1}."
            color = c(p.family)
            solved = f"{len(p.solved_locations)}/{len(LOCATIONS)} solved"
            hp = f"{fmt_hp(p.health)} HP"
            print(f"  {medal} {color}{p.name}{RESET} {emblem(p.family)} — {p.points} pts | {solved} | {hp}")

    def _cmd_families(self):
        print(f"\n{BOLD}The Four Families:{RESET}\n")
        for fid, fam in FAMILIES.items():
            color = c(fid)
            print(f"  {color}{fam['name']}{RESET} {emblem(fid)}")
            print(f"    {DIM}{fam['motto']}{RESET}")
            print(f"    {fam['trait']}\n")

    def _cmd_family_info(self):
        self._cmd_families()

    # ── Help ──────────────────────────────────────────────────────

    def _cmd_help(self):
        print(f"""
{BOLD}Commands:{RESET}

  {BOLD}Exploration{RESET}
    Just type your action!  e.g. 'examine tesla coil', 'open drawer', 'read scroll'
    hint                  Get a hint for the current puzzle stage
    decrypt               [Cyber only] Free code-breaking hint per location
    lore                  [Encyclopedia only] Free historical lore per location
    solve                 Attempt to solve the location (after all clues found)
    locations / loc       View all 100 clues and your progress

  {BOLD}Items & Shop{RESET}
    shop / store          Browse the Underground Market
    buy <item>            Purchase an item (e.g. 'buy sword', 'buy flashlight')
    inventory / inv       Show your items
    use <item>            Use a tool or consumable (e.g. 'use flashlight')
    notes / journal       Review your notepad (requires Pen & Notepad)

  {BOLD}Combat{RESET}
    attack <player/npc>   Attack another player or NPC (requires weapon)
    npcs                  List all 16 roaming rival NPCs

  {BOLD}Character{RESET}
    status / stats        View your character status
    leaderboard / lb      View the global rankings
    families              View family information

  {BOLD}System{RESET}
    save                  Save your progress
    quit / exit           Save and quit the game
    help                  Show this message

{BOLD}How to play:{RESET}
  Each location has a mystery to solve. Examine your surroundings by typing
  actions. Progress through investigation stages to uncover the final answer.
  Solve the final answer to claim the location's points. Use points to buy
  tools, weapons, and defenses.
""")

    # ── Quit ──────────────────────────────────────────────────────

    def _cmd_quit(self):
        self.state.save()
        print(f"\n{GREEN}Progress saved. Until next time, hunter.{RESET}")
        self.running = False

    # ── Helpers ───────────────────────────────────────────────────

    def _current_loc(self):
        """Get the current location dict."""
        idx = self.player.current_location_index
        if idx < len(LOCATIONS):
            return LOCATIONS[idx]
        return None

    def _get_location(self, loc_id: str):
        for loc in LOCATIONS:
            if loc["id"] == loc_id:
                return loc
        return None

    def _show_grand_finale(self):
        fam = FAMILIES[self.player.family]
        color = c(self.player.family)
        print(f"""
{RESET}
  {BOLD}{YELLOW}╔══════════════════════════════════════════════════════════════╗
  ║                                                              ║
  ║              {GREEN}GRAND FINALE — CLUE 100 SOLVED{RESET}                     ║
  ║                                                              ║
  ╚══════════════════════════════════════════════════════════════╝{RESET}

  {BOLD}{color}{self.player.name} of House {fam['name']}{RESET} has reached the final clue —
  the McMurdo Research Station Sub-Ice Vault in Antarctica.

  Inside the ancient ice, a frozen chamber holds the final ingredient
  of the {BOLD}Master Family Serum{RESET}. But as you reach for it, the walls
  illuminate with a holographic message left by the First Hunters...

  {YELLOW}{BOLD}"The serum cannot be activated by one family alone."{RESET}

  {YELLOW}The formula requires four components — one from each house:{RESET}

    {GREEN}Python's venom genetics{RESET}       — the biochemical catalyst
    {RED}Rally's kinetic energy compound{RESET} — the molecular activator
    {CYAN}Cyber's neural nanotechnology{RESET}  — the delivery mechanism
    {YELLOW}Encyclopedia's ancient biological text{RESET} — the instruction code

  {BOLD}THE TWIST:{RESET} The four families were never meant to destroy each
  other. They were {BOLD}meant to unite{RESET}. The century-old war was a test —
  designed by the original patriarchs to determine which bloodline
  was worthy of {BOLD}sharing{RESET} the ultimate prize.

  Only when all four family secrets are combined can the Master
  Family Serum be activated and the true power unlocked.

  {BOLD}{GREEN}House {fam['name']} has been crowned the SUPREME RULERS of the
  four families — the first among equals in a new united order.{RESET}

  The secret war is over. A new era begins.
""")
        self._show_final_leaderboard()

    def _show_final_leaderboard(self):
        print(f"\n{BOLD}{YELLOW}Final Global Leaderboard{RESET}\n")
        board = self.state.get_leaderboard()
        medals = ["\U0001F947", "\U0001F948", "\U0001F949"]
        for i, p in enumerate(board):
            medal = medals[i] if i < 3 else f"  {i+1}."
            color = c(p.family)
            print(f"  {medal} {color}{p.name}{RESET} {emblem(p.family)} — {p.points} pts | {p.solved_count}/{len(LOCATIONS)} solved")
        print(f"\n{BOLD}{GREEN}The global race is complete. The 100 clues have been found.{RESET}")
