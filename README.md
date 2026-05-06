# CPSK Football Game — SKE vs CPE

## Project Description

- **Project by:** Krittitee Chaisang (6810545441)
- **Game Genre:** Sports / 2-Player Local Multiplayer
- **Course:** Computer Programming II (01219116/01219117), Section 450

CPSK Football Game is a local 2-player football game built with Python and Pygame. Two players share one keyboard, select their character skins, and compete in a timed head-to-head match where the goal is to score more than the opponent before time runs out.

The project also includes a data component. Match statistics are recorded to `game_data.csv`, then visualized through a statistics dashboard and an in-game chart viewer so players can review score trends, activity, and match outcomes across multiple rounds.

---

## Installation

Clone the repository:

```sh
git clone https://github.com/Kongbeng-21/CPSK_Football_Game.git
cd CPSK_Football_Game
```

Create and activate a virtual environment, then install dependencies.

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

Run the game:

Mac / Linux:

```sh
python3 main.py
```

Windows:

```bat
python main.py
```

Generate the external statistics dashboard:

Mac / Linux:

```sh
python3 data_analyze.py
```

Windows:

```bat
python data_analyze.py
```

This saves `stats/stats_dashboard.png` and opens a desktop viewer for browsing individual charts.

---

## Tutorial / Usage

### Controls

| Action | Player 1 (SKE) | Player 2 (CPE) |
|--------|----------------|----------------|
| Move   | `A` / `D`      | `Left` / `Right` |
| Jump   | `W`            | `Up` |
| Kick   | `E`            | `Space` |

### Game Flow

1. Start the game to open the main menu.
2. Choose `PLAY`.
3. Both players select a skin and confirm.
4. The match starts after a short countdown.
5. Score by kicking the ball into the opponent's goal.
6. When the timer ends, the result screen appears.
7. Choose to play again or return to the main menu.
8. Choose `STATS` from the menu to open the in-game chart viewer.

---

## Game Features

- 2-player local multiplayer on a single keyboard
- 5 selectable skins: HALAL, VISUS, THE BOY, PARA, BECKHUM
- Ball physics with gravity, bounce, air resistance, and wall reflection
- Timed match flow with countdown and game-over screen
- Animated main menu and tutorial screen
- Per-second match logging to `game_data.csv`
- In-game statistics viewer
- External matplotlib dashboard with 9 charts plus 1 summary table
- Programmatically generated sound effects for match events

---

## Statistics and Visualization

The project records match snapshots over time and uses them to generate visual summaries. The dashboard and chart viewer include:

- Final score by match
- Win rate and win record
- Shot accuracy by match
- Kicks per match
- Jumps per match
- Total shots and touches
- Average score difference over time
- Average possession summary
- Possession versus result comparison
- Summary statistics table

Generated outputs are saved in the `stats/` folder, and supporting screenshots are stored in `screenshots/visualization/`.

---

## Project Structure

- `main.py` — entry point
- `football_game/game.py` — main game controller and state machine
- `football_game/player.py` — player movement, kicking, collisions, rendering
- `football_game/ball.py` — ball physics and drawing
- `football_game/goal.py` — goal detection
- `football_game/menu.py` — main menu and tutorial screen
- `football_game/timer.py` — match timer
- `football_game/data_logger.py` — CSV logging utilities
- `football_game/sound_manager.py` — synthesized sound effects
- `football_game/chart_viewer.py` — in-game chart browser
- `football_game/skin_select.py` — skin selection screen
- `data_analyze.py` — external analysis and dashboard generation

---

## Known Issues

- The repository includes historical match data collected during earlier development iterations. New matches are appended to the same CSV file, so older rows may not follow the latest gameplay tuning exactly.

---

## External Sources

1. Pygame — https://www.pygame.org
2. pandas — https://pandas.pydata.org
3. matplotlib — https://matplotlib.org
4. NumPy — https://numpy.org
5. Character art, field art, and sound assets were generated or synthesized specifically for this project as documented in `DESCRIPTION.md`.
