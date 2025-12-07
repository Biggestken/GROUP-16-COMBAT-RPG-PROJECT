# 🎮 Escape the Streets of Nigeria - RPG Game

An urban survival RPG set in Nigeria with turn-based combat, character progression, and challenging enemies.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Or install pygame directly:
```bash
pip install pygame
```

### 2. Run the Game
```bash
python main.py
```

## 📁 Project Structure

```
nigerian_rpg/
├── main.py              # Main menu and game entry point
├── character.py         # Character class and stats
├── combat.py            # Combat system
├── battle_gui.py        # Battle interface
├── save_system.py       # Save/load functionality
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── assets/             # Game assets (optional)
│   ├── sprites/        # Character and enemy images
│   │   ├── hero.png
│   │   ├── soldier.png
│   │   ├── police.png
│   │   ├── bandit.png
│   │   ├── kidnapper.png
│   │   └── politician.png
│   └── audio/          # Sound effects
│       ├── attack.wav
│       ├── heal.wav
│       ├── victory.wav
│       └── defeat.wav
└── nigerian_rpg.db     # Save file database (auto-created)
```

## 🎯 How to Play

### Character Classes
- **Citizen**: Balanced stats (HP: 100, ATK: 5, DEF: 2)
- **Soldier**: High attack (HP: 120, ATK: 7, DEF: 3)
- **Police**: High defense (HP: 110, ATK: 6, DEF: 4)

### Weapons
- **Cutlass**: Fast special (10 damage threshold)
- **Juju**: Medium special (25 damage threshold)
- **Gun**: Powerful special (50 damage threshold)

### Combat Actions
- **ATTACK**: 90% hit rate, deals weapon damage
- **DEFEND**: 90% success, blocks enemy damage
- **SPECIAL**: Guaranteed hit, 2x weapon damage (limited uses)
- **FLEE**: 60% escape chance

### Game Progression
1. **Level 1**: Forest enemies (Bandits, Area Boys)
2. **Level 2**: City enemies (Kidnappers, Armed Robbers)
3. **Level 3**: Final boss (Politician)

Win all 3 levels to escape!

## 💾 Save System

- Auto-saves every 30 seconds during battle
- Manual saves after each combat
- Load previous games from main menu
- SQLite database storage

## 🎨 Asset Creation (Optional)

The game will run without assets, but you can add custom images and sounds:

### Creating Sprites
- Format: PNG with transparency
- Size: Any (will be scaled automatically)
- Place in `assets/sprites/`

### Creating Sounds
- Format: WAV
- Length: 1-3 seconds recommended
- Place in `assets/audio/`

## ⚙️ Configuration

Edit constants in `battle_gui.py`:
```python
WIDTH, HEIGHT = 960, 600  # Window size
FPS = 30                  # Frame rate
SAVE_INTERVAL = 30000     # Auto-save interval (ms)
```

## 🐛 Troubleshooting

### "No module named 'pygame'"
```bash
pip install pygame
```

### "Cannot load image/sound"
- Assets are optional - game displays colored rectangles without them
- Check file paths match exactly (case-sensitive)
- Ensure assets folders exist: `assets/sprites/`, `assets/audio/`

### "Database is locked"
- Close other instances of the game
- Delete `nigerian_rpg.db` to reset (loses all saves)

### Encoding errors
- All files include `# -*- coding: utf-8 -*-`
- Save files as UTF-8 encoding

## 🎮 Controls

### Main Menu
- Mouse: Click buttons
- Keyboard: Type name, arrow keys for class selection

### Battle
- Mouse: Click action buttons
- Keyboard shortcuts: Coming soon!

### Load Menu
- Mouse: Click save file
- Keyboard: Arrow keys + Enter
- ESC: Cancel

## 📊 Game Stats

- XP required scales with level (×1.3 per level)
- Enemy HP/ATK scales with stage
- Special attacks limited to 3 per battle
- Damage formula: `(Weapon + Roll) - Enemy Defense`

## 🔧 Development

### Adding New Enemies
Edit `battle_gui.py`:
```python
LEVEL_X_ENEMIES = [
    {"name":"Enemy Name", "level":X, "hp":100, "atk":5, "def":2, "sprite":"enemy.png"}
]
```

### Adding New Weapons
Edit `character.py`:
```python
weapon_damages = {
    "New Weapon": 8
}
```

### Adding Skills
Edit character creation in `main.py`:
```python
skills["Skill Name"] = {"power": 10, "type": "damage", "mult": 1.5}
```

## 📝 License

Educational project - Free to use and modify

## 🤝 Credits

Created as a Nigerian-themed RPG learning project

## 📧 Support

For issues, check the troubleshooting section above or review error messages in the console.

---

**Enjoy the game! May you escape the streets! 🎉**
