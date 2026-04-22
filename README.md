# CPSK Football Game — SKE vs CPE

## Project Description

- **Project by:** Krittitee Chaisang (6810545441)
- **Game Genre:** Sports / 2-Player Local Multiplayer
- **Course:** Computer Programming II (01219116/01219117) 2025/2, Section 450

A 2-player head-to-head football game where SKE and CPE face off on the same keyboard.
Players choose their character skin, then compete in a 60-second match to score the most goals.
The game records detailed statistics each second and visualises them in a post-game dashboard.

---

## Installation

**Clone this repository:**
```sh
git clone https://github.com/Kongbeng-21/CPSK_Football_Game.git
cd CPSK_Football_Game
```

**Create and activate a virtual environment:**

Mac / Linux:
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows:
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running Guide

**Run the game:**

Mac / Linux:
```sh
python3 main.py
```

Windows:
```bat
python main.py
```

**Generate statistics dashboard** (after playing at least one match):

Mac / Linux:
```sh
python3 data_analyze.py
```

Windows:
```bat
python data_analyze.py
```

The dashboard is saved to `stats/stats_dashboard.png`.

---

## Tutorial / Usage

### Controls

| Action | Player 1 (SKE) | Player 2 (CPE) |
|--------|---------------|----------------|
| Move   | `A` / `D`     | `←` / `→`      |
| Jump   | `W`           | `↑`            |
| Kick   | `E`           | `Space`        |

### Game Flow

1. Launch the game → **Main Menu**
2. Press `Enter` on **PLAY** → **Skin Selection** screen
3. Both players pick a character skin and confirm
4. A 3-second countdown begins → **Match starts** (60 seconds)
5. Score goals by kicking the ball into the opponent's net
6. When time runs out → **Full Time** screen shows the result
7. Choose **PLAY AGAIN** or **MAIN MENU**
8. View cumulative statistics from the **STATS** option in the menu

---

## Game Features

- **2-player local multiplayer** on a single keyboard
- **5 selectable character skins**: HALAL, VISUS, THE BOY, PARA, BECKHUM
- **Realistic ball physics** — gravity, bounce, air resistance, ground friction
- **60-second timed matches** with live countdown
- **Animated main menu** with floating particles and pitch line overlay
- **How to Play** tutorial screen
- **Per-second statistics logging** to CSV — every match is recorded
- **Statistics dashboard** (9-panel matplotlib visualisation):
  - Final score per match, win rate & win record
  - Shot accuracy, kicks & jumps per match
  - Possession pie chart, score momentum over time
  - Possession vs. result scatter plot with trend line
- **Sound effects** — kick thud and goal cheer

---

## Known Bugs

- Debug name labels (skin name overlay) still visible in-game — to be removed before final submission.

---

## Unfinished Works

- YouTube video presentation (to be recorded before 10 May 2026)
- UML diagram PDF
- VISUALIZATION.md screenshots

---

## External Sources

1. Pygame library — https://www.pygame.org [game framework]
2. Football field image (`assets/field.png`) — original asset
3. Ball image (`assets/ball.png`) — original asset
4. Character head sprites — generated programmatically with Pillow (PIL)
5. Boot sprites — generated programmatically with Pillow (PIL)
