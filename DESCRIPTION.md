# Project Description

## 1. Project Overview

- **Project Name:** CPSK Football Game — SKE vs CPE
- **Brief Description:**

  CPSK Football Game is a 2-player local multiplayer football game developed with Python and Pygame. Two players share one keyboard, choose character skins, and compete in a timed match by kicking a physics-driven ball into the opponent's goal.

  In addition to gameplay, the project includes a data component. Match data is stored in `game_data.csv` and analyzed through both an external dashboard (`data_analyze.py`) and an in-game chart viewer (`football_game/chart_viewer.py`). This allows players to review score trends, player activity, and match results across multiple games.

- **Problem Statement:**
  Many small local multiplayer games focus only on the match itself and provide no meaningful feedback after the round ends. This project aims to combine arcade gameplay with a statistics layer so that players can review performance, compare outcomes, and observe patterns over time.

- **Target Users:**
  Students, friends sharing a computer, and players who want a simple competitive 2-player game with post-match statistics.

- **Key Features:**
  - 2-player local multiplayer on one keyboard
  - 5 selectable player skins
  - Real-time ball physics and collision handling
  - Goal detection and timed match flow
  - Animated menu and tutorial screen
  - Per-second data logging to CSV
  - In-game chart viewer for browsing statistics
  - External dashboard image with multiple charts and a summary table

- **Screenshots:**
  Gameplay screenshots are stored in `screenshots/gameplay/`, and data visualization screenshots are stored in `screenshots/visualization/`.

- **Proposal:**
  [Project Proposal PDF](./6810545441_Programming%202%20(Project%20requirement%20and%20Proposal%20template).pdf)

- **YouTube Presentation:**
  https://youtu.be/m4nKpGndZvg

---

## 2. Concept

### 2.1 Background

This project was inspired by simple competitive football games where two players can start playing immediately without a long learning curve. The SKE versus CPE theme gives the project a clear identity, while the statistics component makes the game more interesting beyond a single round.

Instead of ending the experience when the match is over, the project keeps useful data and turns it into charts. This makes the game feel more complete because players can compare results, observe gameplay patterns, and understand how specific actions relate to winning or losing.

### 2.2 Objectives

- Build a complete playable 2-player football game in Python
- Apply object-oriented programming to separate responsibilities clearly
- Record gameplay data automatically during matches
- Present collected data through readable charts and summaries
- Provide a polished user experience through menus, skin selection, and sound

---

## 3. UML Class Diagram

The UML class diagram is included as a separate PDF file in the repository submission: [UML.pdf](./UML.pdf)

Main class relationships:

- `Game` owns and coordinates `Player`, `Ball`, `Goal`, `Menu`, `Timer`, `DataLogger`, and `SoundManager`
- `Player` interacts with `Ball` through collision and kick behavior
- `SkinManager` contains `Skin` objects for inventory and selection management

---

## 4. Object-Oriented Programming Implementation

| Class | Module | Role |
|-------|--------|------|
| `Game` | `football_game/game.py` | Central controller for the full game loop and state transitions, including menu flow, skin selection, gameplay, results, logging, and chart access |
| `Player` | `football_game/player.py` | Stores player position and movement state, handles jumping and kicking, and manages collisions with the ball and the other player |
| `Ball` | `football_game/ball.py` | Simulates the football using velocity, gravity, bounce, air resistance, and boundary checks |
| `Goal` | `football_game/goal.py` | Represents a goal area and checks whether the ball has entered it |
| `Menu` | `football_game/menu.py` | Draws the animated main menu and handles menu navigation; the same module also contains the tutorial screen drawing function |
| `Timer` | `football_game/timer.py` | Tracks elapsed match time and renders the countdown display |
| `DataLogger` | `football_game/data_logger.py` | Creates the CSV file if needed, maintains headers, determines the next match ID, and appends match rows |
| `SoundManager` | `football_game/sound_manager.py` | Synthesizes and plays match sound effects such as start, goal, timeout, and kick sounds |
| `SkinManager` | `football_game/skin_manager.py` | Stores available skins, player inventories, and equipped skins |
| `Skin` | `football_game/skin_manager.py` | Represents a skin entry containing a name and image surfaces for the player's head and leg |

---

## 5. Statistical Data

### 5.1 Data Recording Method

The project stores gameplay data in `game_data.csv`. Each row represents a time-based gameplay snapshot and is appended by the logging layer during play. The analysis tools read this CSV and aggregate the data by match and by time.

The project provides two ways to view the data:

- `data_analyze.py` generates `stats/stats_dashboard.png` and opens a desktop viewer
- `football_game/chart_viewer.py` renders charts inside the game interface

### 5.2 Data Features

The repository uses the following match data columns:

| Feature | Description |
|---------|-------------|
| `match_id` | Match identifier used to group rows from the same game |
| `time` | Time index of the recorded gameplay snapshot |
| `match_duration` | Total configured match duration for that logged session |
| `ball_speed` | Speed of the ball at that recorded moment |
| `score_p1` | Score of Player 1 / SKE at that moment |
| `score_p2` | Score of Player 2 / CPE at that moment |
| `score_diff` | Difference between `score_p1` and `score_p2` |
| `kicks_p1` | Number of kicks by Player 1 up to that moment |
| `kicks_p2` | Number of kicks by Player 2 up to that moment |
| `jumps_p1` | Number of jumps by Player 1 up to that moment |
| `jumps_p2` | Number of jumps by Player 2 up to that moment |
| `possession` | Possession-related value used by the visualization layer when summarizing control of play |
| `ball_zone` | Zone of the field where the ball is located |
| `attacking_side` | Which side is applying pressure at that moment |
| `touches_p1` | Ball touches by Player 1 |
| `touches_p2` | Ball touches by Player 2 |
| `shots_p1` | Shot attempts by Player 1 |
| `shots_p2` | Shot attempts by Player 2 |
| `winner` | Encoded match result label used by the statistics pipeline |

### 5.3 Visualized Outputs

The dashboard and viewer present:

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

---

## 6. Changed Proposed Features

The final version keeps the original idea of a football game plus statistics, but the implementation was expanded with a stronger presentation layer:

- Added a dedicated skin selection screen
- Added an in-game chart viewer in addition to the exported dashboard image
- Expanded menu presentation and tutorial visuals
- Improved generated sound effects and visual polish

---

## 7. External Sources

### Libraries

- **Pygame** — game framework  
  https://www.pygame.org

- **pandas** — data processing  
  https://pandas.pydata.org

- **matplotlib** — chart rendering  
  https://matplotlib.org

- **NumPy** — numerical processing and sound synthesis  
  https://numpy.org

### Project Assets

- **`assets/field.png`** — generated specifically for this project
- **`assets/ball.png`** — generated specifically for this project
- **Character head sprites** — generated programmatically for this project
- **Boot sprites** — generated programmatically for this project
- **Sound effects** — synthesized programmatically for this project
