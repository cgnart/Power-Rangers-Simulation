
# Power Rangers Megaforce Simulation Report

**Course**: Basic Programming 2  
**Project Topic**: Simulation of a scenario from a film or game  
**Project Title**: Power Rangers Megaforce Enhanced Edition  
**Group Name**: Fay Hattı Studios  
**Team Members**:
- Çağan Deniz Yapıcı (2305041012)
- Kayra Serdar Tosun (2305041034)
- Mahmut Aslan (2305041063)  
**Date**: 28.05.2025

---

## 1. Introduction

This project is a command-line simulation based on the Power Rangers Megaforce universe. The game immerses the player in a role-playing environment where they create a custom Ranger, complete missions, battle enemies, manage resources, and even interact with a simulated stock market. The design reflects a rich integration of the core concepts taught in Basic Programming 2.

---

## 2. System Design Overview

The application is modular and structured around object-oriented principles. The key components include:

- `main.py`: Entry point with the main menu and game loop.
- `character.py`: Defines the PowerRanger class and handles player attributes.
- `enemy.py`: Contains enemy creation logic.
- `battle.py`: Manages the turn-based combat system.
- `mission.py`: Handles missions and progress tracking.
- `stock_market.py`: Implements a mock financial system with random stock prices.
- `save_system.py`: Allows saving/loading of game progress using JSON.
- `utils.py`: Contains helper functions.
- `config.py`: Stores constants and bonus configurations.

---

## 3. Key Programming Concepts Used

- **Object-Oriented Programming**
  - Classes and objects (PowerRanger, Enemy, BattleSystem, etc.)
  - Encapsulation and modularity.
  - Inheritance and method overriding for different character behaviors.

- **Functional Programming**
  - Use of `lambda`, `map`, `filter`, and `reduce` where applicable (e.g., filtering missions or stock market data).

- **Modules & Packages**
  - Codebase organized into logical modules for better readability and maintenance.

- **File I/O & Persistence**
  - Game states are saved and loaded using JSON format in a dedicated `saves` folder.

- **Error Handling**
  - Use of try/except blocks across menus and systems.
  - Prevents crashes on invalid input or corrupted files.

- **Time & Utility Modules**
  - Uses `random` for randomness in battles and stock values.
  - `time` for delays and animation effects.

---

## 4. Gameplay Features & Mechanics (Detailed)

- **Character Customization**
  - Players choose a name, ranger color (each with different health and attack bonuses), and a power type (such as tech, magic, or nature).

- **Battle System**
  - Turn-based combat.
  - Players and enemies attack each other using basic and special skills.
  - Combat stats (health, attack, defense) vary based on ranger color and level.
  - Players gain experience points and gold by winning.

- **Fusion Power System**
  - Special skill called "Fusion Power" becomes available only when the player reaches **level 3 or above**.
  - Requires accumulation of **3 Mega Energy** points, which are gained during normal combat turns.
  - When triggered, Fusion Power deals a massive attack and heals the Ranger partially.
  - After activation, Mega Energy resets to 0.

- **Mission System**
  - Randomly assigned tasks with different goals (e.g., defeat a number of enemies, collect resources).
  - Rewards include XP, gold, and sometimes rare boosts.
  - Difficulty scales with player level.

- **Stock Market Simulation**
  - Players can buy and sell shares of fictional companies.
  - Prices change randomly each turn.
  - Encourages risk/reward strategy for gaining gold.

- **Save/Load System**
  - Players can save their progress at any point.
  - JSON-based file system allows for structured, persistent storage.

---

## 5. Conclusion

This project successfully integrates nearly all core topics from the course into a cohesive and playable simulation. It demonstrates advanced command-line interaction, object modeling, error handling, and data persistence. The complexity and scale of the project go beyond minimal requirements and showcase effective teamwork and software design.

### Planned Improvements (if more time):
- Add unit testing for battle and save systems.
- Implement a leaderboard or high-score system.
- Expand stock market with trends or news.
- Add more unique Fusion Powers per color or class.

---

**End of Report**
