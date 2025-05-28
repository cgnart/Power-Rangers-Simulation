# Game Configuration
class Config:
    # Character Stats
    BASE_HEALTH = 100
    BASE_ATTACK = 20
    BASE_DEFENSE = 10
    BASE_SPEED = 15
    
    # Color Bonuses
    COLOR_BONUSES = {
        "Red": {"health": 10, "attack": 5, "leadership": True},
        "Blue": {"health": 5, "defense": 5, "strategy": True},
        "Yellow": {"health": 8, "speed": 5, "agility": True},
        "Pink": {"health": 6, "attack": 3, "healing": True},
        "Black": {"health": 7, "defense": 3, "stealth": True},
        "Green": {"health": 9, "attack": 4, "nature": True}
    }
    
    # Power Type Bonuses
    POWER_BONUSES = {
        "Megaforce": {"attack": 5, "special": "Mega Blast"},
        "Super Megaforce": {"attack": 8, "special": "Super Mega Cannon"},
        "Mystic Force": {"attack": 6, "special": "Mystic Spell"},
        "Ninja Storm": {"speed": 8, "special": "Ninja Strike"},
        "Dino Thunder": {"health": 10, "special": "Dino Roar"},
        "Time Force": {"defense": 7, "special": "Time Freeze"}
    }
    
    # Weapon Stats
    WEAPON_STATS = {
        "Power Sword": {"damage": 15, "speed": 0, "special": "Sword Slash"},
        "Power Blaster": {"damage": 12, "speed": 3, "special": "Energy Blast"},
        "Dragon Dagger": {"damage": 18, "speed": -2, "special": "Dragon Fire"},
        "Shark Fin": {"damage": 20, "speed": -5, "special": "Shark Attack"},
        "Phoenix Shot": {"damage": 14, "speed": 2, "special": "Phoenix Flame"},
        "Snake Axe": {"damage": 22, "speed": -3, "special": "Venom Strike"}
    }
    
    # XP and Leveling
    XP_PER_LEVEL = 100
    LEVEL_STAT_BONUS = 5
    MAX_LEVEL = 50
    
    # Stock Market
    INITIAL_COMMODITIES = {
        "Gold": {"price": 100, "volatility": 0.1},
        "Silver": {"price": 50, "volatility": 0.15},
        "Crypto": {"price": 200, "volatility": 0.25},
        "Energy Crystals": {"price": 150, "volatility": 0.2},
        "Morphin Grid": {"price": 300, "volatility": 0.3}
    }
    
    # Battle Settings
    COMBO_KEYS = ['W', 'A', 'S', 'D', 'Q', 'E']
    COMBO_TIME_LIMIT = 3.0
    COMBO_DAMAGE_MULTIPLIER = 2.0
    
    # Mission Settings
    MISSION_TYPES = ["City Defense", "Forest Battle", "Space Base", "Underwater", "Mountain Peak"]
    MISSION_DIFFICULTIES = ["Easy", "Medium", "Hard", "Extreme"]
    
    # Enemy Settings
    ENEMY_TYPES = {
        "Loogies": {"health": 30, "attack": 8, "behavior": "aggressive"},
        "Zombats": {"health": 25, "attack": 10, "behavior": "swarm"},
        "Bruisers": {"health": 60, "attack": 15, "behavior": "tank"},
        "X-Borgs": {"health": 45, "attack": 12, "behavior": "tactical"}
    }
    
    # Boss Settings
    BOSS_ENEMIES = {
        "Metal Alice": {"health": 200, "attack": 25, "phases": 2},
        "Black Knight": {"health": 250, "attack": 30, "phases": 3},
        "Emperor Mavro": {"health": 300, "attack": 35, "phases": 3}
    }
