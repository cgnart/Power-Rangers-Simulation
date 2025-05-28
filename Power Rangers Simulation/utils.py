"""
Utility functions for the Power Rangers Enhanced Game
"""

import random
import time
from typing import List, Dict, Any, Callable
from functools import reduce
from itertools import combinations, chain
from collections import Counter, defaultdict

def colored_text(text: str, color: str) -> str:
    """Return colored text for terminal output"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'bold': '\033[1m',
        'end': '\033[0m'
    }
    
    return f"{colors.get(color, '')}{text}{colors['end']}"

def create_health_bar(current: int, maximum: int, length: int = 20) -> str:
    """Create a visual health bar"""
    filled = int((current / maximum) * length)
    bar = "█" * filled + "░" * (length - filled)
    return f"[{bar}] {current}/{maximum}"

def create_progress_bar(current: int, maximum: int, length: int = 10) -> str:
    """Create a progress bar with different characters"""
    filled = int((current / maximum) * length)
    bar = "⚡" * filled + "░" * (length - filled)
    return f"[{bar}] {current}/{maximum}"

def format_number(number: int) -> str:
    """Format large numbers with commas"""
    return f"{number:,}"

def calculate_damage_reduction(defense: int, damage: int) -> int:
    """Calculate damage after defense reduction"""
    reduction = min(defense * 0.5, damage * 0.8)  # Max 80% reduction
    return max(1, int(damage - reduction))

# Functional Programming Examples
def calculate_damage(base_damage: int, modifiers: List[float]) -> int:
    """Calculate final damage using functional programming with reduce"""
    # Use reduce to apply all damage modifiers
    final_damage = reduce(lambda damage, modifier: damage * modifier, modifiers, base_damage)
    return max(1, int(final_damage))

def apply_status_effect(character, effect_type: str, duration: int) -> bool:
    """Apply status effect using functional approach"""
    # Use lambda to create effect object
    create_effect = lambda etype, dur: {"type": etype, "duration": dur, "timestamp": time.time()}
    
    # Filter out existing effects of same type
    character.status_effects = list(filter(lambda e: e["type"] != effect_type, character.status_effects))
    
    # Add new effect
    character.status_effects.append(create_effect(effect_type, duration))
    return True

def is_critical_hit(attack_power: int, luck_factor: float = 0.1) -> bool:
    """Determine if attack is critical using functional approach"""
    # Use lambda for critical calculation
    crit_chance = lambda power, luck: min(0.3, (power / 100) * luck)
    return random.random() < crit_chance(attack_power, luck_factor)

def filter_valid_targets(targets: List[Dict], condition: Callable) -> List[Dict]:
    """Filter valid targets using functional programming"""
    return list(filter(condition, targets))

def map_damage_to_enemies(enemies: List[Dict], damage_func: Callable) -> List[int]:
    """Map damage calculation to multiple enemies"""
    return list(map(damage_func, enemies))

def calculate_total_stats(characters: List[Dict]) -> Dict[str, int]:
    """Calculate total stats using functional programming"""
    # Use map to extract stats, then reduce to sum them
    get_stat = lambda char, stat: char.get(stat, 0)
    
    stats = ['health', 'attack', 'defense', 'speed']
    totals = {}
    
    for stat in stats:
        stat_values = map(lambda char: get_stat(char, stat), characters)
        totals[stat] = reduce(lambda a, b: a + b, stat_values, 0)
    
    return totals

def find_best_combination(items: List[Dict], max_cost: int) -> List[Dict]:
    """Find best combination of items within budget using itertools"""
    from itertools import combinations
    
    valid_combinations = []
    
    # Generate all possible combinations
    for r in range(1, len(items) + 1):
        for combo in combinations(items, r):
            total_cost = sum(item['cost'] for item in combo)
            if total_cost <= max_cost:
                total_value = sum(item['value'] for item in combo)
                valid_combinations.append((combo, total_value, total_cost))
    
    # Return best combination by value
    if valid_combinations:
        best_combo = max(valid_combinations, key=lambda x: x[1])
        return list(best_combo[0])
    return []

def analyze_battle_patterns(battle_history: List[Dict]) -> Dict[str, Any]:
    """Analyze battle patterns using collections"""
    if not battle_history:
        return {}
    
    # Use Counter for frequency analysis
    results = Counter(battle['result'] for battle in battle_history)
    enemies = Counter(battle['enemy'] for battle in battle_history)
    
    # Use defaultdict for grouping
    battles_by_enemy = defaultdict(list)
    for battle in battle_history:
        battles_by_enemy[battle['enemy']].append(battle)
    
    # Calculate win rates per enemy
    win_rates = {}
    for enemy, battles in battles_by_enemy.items():
        wins = sum(1 for b in battles if b['result'] == 'victory')
        win_rates[enemy] = wins / len(battles) if battles else 0
    
    return {
        'total_battles': len(battle_history),
        'result_counts': dict(results),
        'enemy_counts': dict(enemies),
        'win_rates_by_enemy': win_rates,
        'most_common_enemy': enemies.most_common(1)[0] if enemies else None,
        'overall_win_rate': results['victory'] / len(battle_history) if battle_history else 0
    }

def generate_battle_cry() -> str:
    """Generate random Power Rangers battle cry"""
    cries = [
        "Go Go Megaforce!",
        "It's Morphin Time!",
        "Megaforce Red, ready!",
        "Power Rangers, unite!",
        "Let's show them Ranger power!",
        "Earth's defenders, attack!",
        "Megaforce, charge!",
        "Rangers together, samurai forever!",
        "Defender mode, activate!",
        "Ultra mode, engage!"
    ]
    return random.choice(cries)

def generate_enemy_taunt() -> str:
    """Generate random enemy taunt"""
    taunts = [
        "You cannot stop the Armada!",
        "Prepare for destruction, Rangers!",
        "Your planet will fall!",
        "Resistance is futile!",
        "The Emperor will have his victory!",
        "You are no match for our power!",
        "Soon, Earth will be ours!",
        "Your Ranger powers are weak!",
        "Surrender now and we might spare you!",
        "The Armada's might is unstoppable!"
    ]
    return random.choice(taunts)

def dramatic_pause(duration: float = 1.0):
    """Create dramatic pause for better game flow"""
    time.sleep(duration)

def typewriter_effect(text: str, delay: float = 0.03):
    """Print text with typewriter effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # New line at the end

def display_ascii_art(art_type: str) -> str:
    """Return ASCII art for various game elements"""
    art_collection = {
        'victory': """
    🎉 VICTORY! 🎉
    ╔══════════════╗
    ║   YOU WIN!   ║
    ╚══════════════╝
        """,
        
        'defeat': """
    💀 DEFEAT 💀
    ╔══════════════╗
    ║  GAME OVER   ║
    ╚══════════════╝
        """,
        
        'level_up': """
    ⭐ LEVEL UP! ⭐
    ╔══════════════╗
    ║ POWER BOOST! ║
    ╚══════════════╝
        """,
        
        'combo': """
    ⚡ COMBO! ⚡
    ╔══════════════╗
    ║ SUPER ATTACK ║
    ╚══════════════╝
        """,
        
        'critical': """
    💥 CRITICAL! 💥
    ╔══════════════╗
    ║ MASSIVE DMG! ║
    ╚══════════════╝
        """,
        
        'mission_complete': """
    🏆 MISSION COMPLETE! 🏆
    ╔════════════════════╗
    ║   OBJECTIVE DONE   ║
    ╚════════════════════╝
        """
    }
    
    return art_collection.get(art_type, "")

def calculate_battle_rating(victories: int, defeats: int, level: int) -> str:
    """Calculate player's battle rating"""
    total_battles = victories + defeats
    if total_battles == 0:
        return "Rookie"
    
    win_rate = victories / total_battles
    
    if level >= 10 and win_rate >= 0.9:
        return "Legendary Ranger"
    elif level >= 8 and win_rate >= 0.8:
        return "Elite Ranger"
    elif level >= 6 and win_rate >= 0.7:
        return "Veteran Ranger"
    elif level >= 4 and win_rate >= 0.6:
        return "Skilled Ranger"
    elif level >= 2 and win_rate >= 0.5:
        return "Experienced Ranger"
    else:
        return "Rookie Ranger"

def generate_loot_description(gold: int, xp: int) -> str:
    """Generate descriptive loot text"""
    descriptions = []
    
    if gold > 0:
        if gold >= 500:
            descriptions.append(f"💰 Massive treasure hoard: {gold} gold!")
        elif gold >= 200:
            descriptions.append(f"💰 Valuable loot: {gold} gold!")
        else:
            descriptions.append(f"💰 Small reward: {gold} gold")
    
    if xp > 0:
        if xp >= 200:
            descriptions.append(f"⭐ Incredible experience: {xp} XP!")
        elif xp >= 100:
            descriptions.append(f"⭐ Great experience: {xp} XP!")
        else:
            descriptions.append(f"⭐ Experience gained: {xp} XP")
    
    return " | ".join(descriptions)

def validate_save_integrity(save_data: Dict[str, Any]) -> List[str]:
    """Validate save file integrity and return list of issues"""
    issues = []
    
    # Check required top-level keys
    required_keys = ["character", "stock_market", "save_timestamp"]
    for key in required_keys:
        if key not in save_data:
            issues.append(f"Missing required key: {key}")
    
    # Check character data
    if "character" in save_data:
        char_data = save_data["character"]
        required_char_keys = ["name", "level", "max_health", "current_health", "gold"]
        for key in required_char_keys:
            if key not in char_data:
                issues.append(f"Missing character data: {key}")
        
        # Validate ranges
        if "level" in char_data and char_data["level"] < 1:
            issues.append("Invalid character level")
        if "current_health" in char_data and char_data["current_health"] < 0:
            issues.append("Invalid current health")
        if "gold" in char_data and char_data["gold"] < 0:
            issues.append("Invalid gold amount")
    
    # Check stock market data
    if "stock_market" in save_data:
        market_data = save_data["stock_market"]
        if "commodities" not in market_data:
            issues.append("Missing stock market commodities")
    
    return issues

def format_time_played(start_time: float) -> str:
    """Format elapsed time in a readable format"""
    elapsed = time.time() - start_time
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def get_difficulty_modifier(player_level: int, enemy_level: int) -> float:
    """Calculate difficulty modifier based on level difference"""
    level_diff = enemy_level - player_level
    
    if level_diff >= 3:
        return 1.5  # Much harder
    elif level_diff >= 1:
        return 1.2  # Harder
    elif level_diff <= -3:
        return 0.7  # Much easier
    elif level_diff <= -1:
        return 0.8  # Easier
    else:
        return 1.0  # Same level

def generate_random_event() -> Dict[str, Any]:
    """Generate random events for the game"""
    events = [
        {
            "name": "Mysterious Merchant",
            "description": "A mysterious merchant offers you a rare item!",
            "type": "merchant",
            "effect": {"gold": -100, "item": "rare_crystal"}
        },
        {
            "name": "Lucky Find",
            "description": "You found a hidden cache of gold!",
            "type": "treasure",
            "effect": {"gold": 150}
        },
        {
            "name": "Training Opportunity",
            "description": "An experienced Ranger offers training!",
            "type": "training",
            "effect": {"xp": 75}
        },
        {
            "name": "Market Crash",
            "description": "The stock market experiences volatility!",
            "type": "market",
            "effect": {"market_volatility": 0.2}
        }
    ]
    
    return random.choice(events)

# Combat calculation utilities
def calculate_critical_damage(base_damage: int, crit_multiplier: float = 1.5) -> int:
    """Calculate critical hit damage"""
    return int(base_damage * crit_multiplier)

def calculate_dodge_success(dodge_chance: float, attacker_accuracy: float = 1.0) -> bool:
    """Determine if an attack is dodged"""
    effective_dodge = dodge_chance / attacker_accuracy
    return random.random() < effective_dodge

def calculate_status_duration(base_duration: int, resistance: float = 0.0) -> int:
    """Calculate how long a status effect lasts"""
    modified_duration = base_duration * (1 - resistance)
    return max(1, int(modified_duration))

# Game balance utilities
def scale_enemy_stats(base_stats: Dict[str, int], level: int) -> Dict[str, int]:
    """Scale enemy stats based on level"""
    scaling_factor = 1 + (level - 1) * 0.15
    scaled_stats = {}
    
    for stat, value in base_stats.items():
        scaled_stats[stat] = int(value * scaling_factor)
    
    return scaled_stats

def calculate_xp_requirement(level: int) -> int:
    """Calculate XP required for next level"""
    base_xp = 100
    return int(base_xp * (1.2 ** (level - 1)))

def get_recommended_level(area: str) -> int:
    """Get recommended level for different areas"""
    area_levels = {
        "City": 1,
        "Forest": 2,
        "Space Base": 4,
        "Command Center": 3,
        "Final Battle": 7
    }
    return area_levels.get(area, 1)

# Advanced functional programming examples
def optimize_skill_usage(available_skills: List[Dict], mega_energy: int) -> List[str]:
    """Optimize skill usage based on available mega energy using functional programming"""
    # Filter skills by energy cost
    affordable_skills = list(filter(lambda skill: skill['cost'] <= mega_energy, available_skills))
    
    # Sort by effectiveness (damage/cost ratio)
    effectiveness = lambda skill: skill['damage'] / skill['cost'] if skill['cost'] > 0 else skill['damage']
    optimal_skills = sorted(affordable_skills, key=effectiveness, reverse=True)
    
    # Use itertools to find best combination
    from itertools import combinations
    best_combo = []
    best_value = 0
    
    for r in range(1, len(optimal_skills) + 1):
        for combo in combinations(optimal_skills, r):
            total_cost = sum(skill['cost'] for skill in combo)
            if total_cost <= mega_energy:
                total_damage = sum(skill['damage'] for skill in combo)
                if total_damage > best_value:
                    best_value = total_damage
                    best_combo = [skill['name'] for skill in combo]
    
    return best_combo

def chain_attacks(attack_sequences: List[List[str]]) -> List[str]:
    """Chain multiple attack sequences using itertools.chain"""
    from itertools import chain
    return list(chain.from_iterable(attack_sequences))

def group_enemies_by_type(enemies: List[Dict]) -> Dict[str, List[Dict]]:
    """Group enemies by type using collections.defaultdict"""
    from collections import defaultdict
    grouped = defaultdict(list)
    
    for enemy in enemies:
        grouped[enemy['type']].append(enemy)
    
    return dict(grouped)
