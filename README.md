# Retro Arcade

A neon arcade hub — 8 games, one cabinet. Open `index.html` and play.

## Games

| # | Game | Notes |
|---|------|-------|
| 1 | 🎲 Dice & Boxes Duel | 2-player hotseat board duel |
| 2 | 🧪 Elemental Merge | Merge units, fight waves, defend your base |
| 3 | 💣 Bomb Battle | Neon paddle duel vs the CPU |
| 4 | 🕵️ Clue Hunt | Terminal mystery — solo works anywhere; multiplayer needs its server (`bash games/clue-hunt/start.sh`) |
| 5 | 🗼 GameTower | 20 floors of arcade challenges, 3 lives |
| 6 | 🐛 Chaos Bug Hunt | Jet shooter — hunt the bugs, beat the boss |
| 7 | 🧙 Hogwarts Game Room | Hosted at [jianran.github.io/hogwarts-game-room](https://jianran.github.io/hogwarts-game-room/) |
| 8 | ⛄ Snowman Bros | Platformer for 1–2 players |

## Tokens

- 5 free tokens per day — unused ones stack up
- Elemental Merge and Chaos Bug Hunt cost 3 tokens; all other games cost 1
- Buy 5 tokens for ₩1,000 in the Token Shop (🪙 button, top right) — via Toss Payments once automatic payments are switched on; until then the honor-system "I've paid" button works, optionally enforced with signed top-up codes from `topup.html`
- Automatic verified payments are built and ready (Supabase backend + PayPal checkout; an Alipay 当面付 variant also lives in the repo) — see `SETUP.md`
- Top-up codes: the arcade owner generates redeem links/strings with the private `topup.html` generator (kept out of this repo on purpose). The public site only holds the verification key, so codes can't be forged from the source. Each purchase gets a unique one, works once per device, and expires after a day.
- Balances live in Supabase (server-side) once the backend is enabled; the offline fallback uses localStorage per browser.

## Run locally

Double-click `index.html`, or serve it:

```bash
bash start.sh          # → http://127.0.0.1:8137/
```

Keys `1`–`8` launch games from the hub.
