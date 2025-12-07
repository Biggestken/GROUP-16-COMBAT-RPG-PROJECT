# ⚔️ Nigerian Urban RPG - Escape the Streets

A Nigerian-themed turn-based combat RPG built with Python and Pygame.

## 🎮 Game Features

- 3 Character Classes: Citizen, Soldier, Police
- 3 Weapons: Juju, Cutlass, Gun
- 3 Levels: Forest → City → Government Building
- Animated Sprites: Damage and victory animations
- Settings System: Sound, music, effects, and difficulty options
- Leaderboard: Track fastest times, highest damage, and most kills
- Save/Load System: Multiple save slots with auto-save

## 🎯 Gameplay

Battle through 3 levels of Nigerian-themed enemies:
- Level 1: Bandit / Area Boy (Forest)
- Level 2: Kidnapper / Armed Robber (City)
- Level 3: Politician (Final Boss)

### Combat Actions:
- Attack - 90% hit chance
- Defend - Block incoming damage
- Special - Unique weapon abilities
- Flee - Escape the battle

## 🛠️ Installation

### Requirements:
- Python 3.8+
- Pygame

### Setup:
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/nigerian-urban-rpg.git
cd nigerian-urban-rpg

# Install dependencies
pip install pygame

# Run the game
python main.py
```

## 📦 Creating an Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "assets;assets" --name "NigerianRPG" main.py
```

The executable will be in the `dist/` folder.

## 🎨 Screenshots

![Main Menu](screenshots/menu.png)
![Battle Screen](screenshots/battle.png)
![Leaderboard](screenshots/leaderboard.png)

## 📁 Project Structure
```
nigerian-urban-rpg/
├── main.py              # Main menu and launcher
├── battle_gui.py        # Battle interface with animations
├── character.py         # Character class and stats
├── combat.py            # Combat logic and AI
├── save_system.py       # Save/load and database
├── animation.py         # Animation system (optional)
├── resources.py         # Asset manager (optional)
├── assets/
│   ├── sprites/         # Character sprites
│   └── audio/           # Sound effects
└── README.md
```

## Team Members

- Adewuyi Kehinde J.
- Fabumi Ifedolapo
- Maureen
- Haruna Yushau 

## Course Information

Course: Python Advanced
Instructor: Mr J.
Institution: NCAIR
Date: December 2025

## 📜 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Pygame community
- Nigerian cultural elements and themes

