# Project Description

## 1. Project Overview

- **Project Name:** CPSK Football Game — SKE vs CPE
- **Brief Description:**

  CPSK Football Game is a 2-player local-multiplayer football (soccer) game built with Python and Pygame.
  Two players share a keyboard and compete in a 60-second match, each trying to kick a physics-simulated
  ball into the opponent's goal. Players can choose from five distinct character skins before each match.

  Beyond the game itself, the project includes a data component: every second of every match is logged
  to a CSV file. A separate analysis script reads this data and generates a 9-panel statistics dashboard
  that shows win rates, shot accuracy, possession, kicks, jumps, and gameplay momentum over time.

- **Problem Statement:**
  Many simple 2-player games lack a statistical feedback loop. This project combines accessible arcade
  gameplay with meaningful post-match data visualisation, letting players see how their performance
  evolves across sessions.

- **Target Users:** Two players sharing a computer, students in a lab setting, or anyone wanting a
  quick competitive local multiplayer experience.

- **Key Features:**
  - 2-player local multiplayer on a single keyboard
  - 5 selectable character skins with individual head and boot designs
  - Real-time ball physics (gravity, bounce, air resistance, wall reflection)
  - 60-second timed matches with live countdown and goal detection
  - Animated main menu with football pitch overlay and particle effects
  - Per-second statistics logging (19 features) saved to `game_data.csv`
  - 9-panel matplotlib statistics dashboard generated from historical match data
  - Sound effects for kicks and goals

- **Screenshots:** *(add gameplay and data screenshots in `screenshots/` folder)*

- **Proposal:** [Project Proposal PDF](./6810545441_Programming%202%20(Project%20requirement%20and%20Proposal%20template).pdf)

- **YouTube Presentation:** *(link to be added)*

---

## 2. Concept

### 2.1 Background

The project was inspired by classic head-to-head browser football games (e.g., Head Soccer) and the
friendly rivalry between SKE and CPE departments at Kasetsart University. The goal was to build
something that is immediately fun to pick up while also having a deeper data layer — something
that makes re-playing the game worthwhile beyond just the gameplay itself.

Collecting and visualising match statistics turns every session into a small experiment: Does
having more possession lead to winning? Does shot accuracy improve over multiple matches? These
questions make the data component meaningful rather than decorative.

### 2.2 Objectives

- Implement a complete, playable 2-player football game with real-time physics
- Apply object-oriented design principles across all game components
- Record detailed per-second match statistics automatically during gameplay
- Visualise the collected data with clear, informative charts and summaries
- Provide a polished user experience: animated menus, skin selection, sound effects

---

## 3. UML Class Diagram

*(Attach as PDF — see `UML.pdf`)*

The diagram includes the following classes and their relationships:

- `Game` aggregates `Player` (×2), `Ball`, `Goal` (×2), `Menu`, `Timer`, `DataLogger`, `SoundManager`
- `SkinManager` composes `Skin` objects and is used during skin selection
- `Player` depends on `Ball` for collision and kick logic

---

## 4. Object-Oriented Programming Implementation

| Class | Module | Role |
|-------|--------|------|
| `Game` | `football_game/game.py` | Central controller — manages the state machine (menu → skin select → countdown → gameplay → game over → stats), coordinates all subsystems, and holds the main game loop |
| `Player` | `football_game/player.py` | Represents a player character. Handles movement input, jump physics, kick mechanics, collision with the ball and other player, and sprite rendering |
| `Ball` | `football_game/ball.py` | Simulates ball physics — gravity, air resistance, ground friction, wall/ground bounce — and handles drawing |
| `Goal` | `football_game/goal.py` | Defines a goal area (left or right) and checks whether the ball has entered it |
| `Menu` | `football_game/menu.py` | Renders the animated main menu (pitch stripes, floating particles, pulsing VS badge, navigation buttons). Also provides the `draw_tutorial()` function for the How To Play screen |
| `Timer` | `football_game/timer.py` | Tracks elapsed match time, provides a `time_left` value, and renders the on-screen countdown |
| `DataLogger` | `football_game/data_logger.py` | Creates and appends rows to `game_data.csv`. Manages match IDs and CSV headers |
| `SoundManager` | `football_game/sound_manager.py` | Synthesises and plays sound effects (kick thud, goal cheer) using NumPy arrays; falls back to WAV files in `assets/sounds/` if present |
| `SkinManager` | `football_game/skin_manager.py` | Manages a pool of `Skin` objects, player inventories, and currently equipped skins |
| `Skin` | `football_game/skin_manager.py` | Data class holding a skin's name and its head/leg pygame Surface images |

---

## 5. Statistical Data

### 5.1 Data Recording Method

`DataLogger` appends one CSV row per second of gameplay (triggered by `log_stats_once_per_second()`
inside the main game loop). Each row captures a snapshot of the match state at that second.
Data is stored in `game_data.csv` at the project root and persists across sessions.

### 5.2 Data Features

| Feature | Description |
|---------|-------------|
| `match_id` | Unique integer ID, incremented each new game |
| `time` | Elapsed seconds since match start (0–60) |
| `match_duration` | Total match duration (always 60) |
| `ball_speed` | Euclidean speed of the ball (√(vx²+vy²)) |
| `score_p1` | Goals scored by SKE (Player 1) |
| `score_p2` | Goals scored by CPE (Player 2) |
| `score_diff` | `score_p1 − score_p2` |
| `kicks_p1` | Cumulative kicks by SKE |
| `kicks_p2` | Cumulative kicks by CPE |
| `jumps_p1` | Cumulative jumps by SKE |
| `jumps_p2` | Cumulative jumps by CPE |
| `possession` | Approximate possession % for SKE (distance-based) |
| `ball_zone` | Current ball zone: LEFT / CENTER / RIGHT |
| `attacking_side` | SKE_ATTACK / CPE_ATTACK / NEUTRAL |
| `touches_p1` | Cumulative ball touch events for SKE |
| `touches_p2` | Cumulative ball touch events for CPE |
| `shots_p1` | Shots on goal by SKE (kicks aimed toward CPE net) |
| `shots_p2` | Shots on goal by CPE |
| `winner` | Match result: `p1` / `p2` / `draw` |

The analysis script (`data_analyze.py`) aggregates this data across all matches and produces
a 9-panel dashboard saved to `stats/stats_dashboard.png`.

---

## 6. Changed Proposed Features

*(Fill in if any features differ from the original proposal)*

---

## 7. External Sources

### AI-Generated Assets
- **assets/field.png** — Generated with Google Gemini  
  Prompt: "Generate a top-down football/soccer pitch with dirt/earth theme 
  for use as a background in a Pygame game. Include field markings, 
  penalty areas, center circle, and CPSK and KU85 signage on the sidelines."

- **assets/ball.png** — Generated with Google Gemini  
  Prompt: "Draw a simple cartoon soccer ball for use in a Pygame game."

- **Character head sprites** (halal_head.png, visus_head.png, theboy_head.png, 
  para_head.png, beckhum_head.png) — Generated programmatically with Python/Pillow.  
  Character designs inspired by (not copied from) real footballers:  
  HALAL → Erling Haaland, VISUS → Vinícius Jr., THE BOY → Kevin De Bruyne,  
  PARA → Mohamed Salah, BECKHUM → David Beckham

- **Boot sprites** (*_leg.png) — Generated programmatically with Python/Pillow

- **Sound effects** (kick.wav, goal.wav, etc.) — Synthesised programmatically with NumPy
