# Power Rangers Simulation
## 🎮 Project Overview
This is a terminal-based simulation game inspired by the Power Rangers Megaforce universe. Designed for the Basic Programming 2 course, it includes RPG elements, a turn-based battle system, mission mechanics, and a simulated stock market—all implemented in Python using core programming concepts.

## 🧠 Key Features
- **Character Customization**: Choose name, ranger color (with unique bonuses), and power type.
- **Battle System**: Turn-based combat featuring health, attack, defense, and XP mechanics.
- **Fusion Power**: Unlockable special skill after level 3 and 3 Mega Energy points.
- **Mission System**: Randomly generated tasks with rewards based on difficulty.
- **Stock Market**: Buy/sell shares with randomized price fluctuations.
- **Save/Load**: Full progress tracking with JSON-based save files.

## 🧩 Tech Used
- Python 3
- OOP (classes, inheritance)
- Functional Programming (`map`, `filter`, `lambda`)
- File I/O (JSON)
- Modular Design
- Error Handling (`try/except`)
- Utility Modules: `random`, `time`

## 👥 Team (Fay Hattı Studios)
- Çağan Deniz Yapıcı (2305041012)
- Kayra Serdar Tosun (2305041034)
- Mahmut Aslan (2305041063)

## 🗂️ Project Structure
```
├── main.py               # Main menu and game loop
├── character.py          # PowerRanger class
├── enemy.py              # Enemy generation
├── battle.py             # Battle mechanics
├── mission.py            # Missions logic
├── stock_market.py       # Simulated trading
├── save_system.py        # Save/load game progress
├── utils.py              # Helper functions
├── config.py             # Constants and bonuses
└── saves/                # Save files (.json)
```

## 🚀 How to Run
```bash
python main.py
```

## 📈 Future Improvements
- Add automated unit testing
- Implement leaderboard system
- Expand stock market with trends/news
- Introduce more Fusion Power types based on ranger color

---

🛡️ Made with passion by Fay Hattı Studios

