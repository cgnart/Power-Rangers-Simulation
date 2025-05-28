import random
from enum import Enum
from config import Config
from abc import ABC, abstractmethod

class EnemyState(Enum):
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    FLEEING = "fleeing"
    STUNNED = "stunned"
    ENRAGED = "enraged"

# Base Enemy class with inheritance and polymorphism
class Enemy(ABC):
    """Abstract base class for all enemies"""
    
    def __init__(self, name, enemy_type="basic"):
        self.name = name
        self.enemy_type = enemy_type
        self.max_health = 50
        self.current_health = self.max_health
        self.attack = 15
        self.defense = 5
        self.speed = 10
        self.gold_reward = 25
        self.xp_reward = 20
        
        # AI and Behavior
        self.state = EnemyState.AGGRESSIVE
        self.behavior_pattern = "normal"
        self.turn_counter = 0
        
        # Limb System
        self.limbs = {
            "left_arm": {"health": 20, "max_health": 20, "broken": False},
            "right_arm": {"health": 20, "max_health": 20, "broken": False},
            "left_leg": {"health": 15, "max_health": 15, "broken": False},
            "right_leg": {"health": 15, "max_health": 15, "broken": False}
        }
        
        # Status Effects
        self.status_effects = []
        self.special_abilities = []
        
        # Apply type-specific stats
        self._apply_type_stats()
    
    @abstractmethod
    def get_special_attack(self):
        """Abstract method for special attacks - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def get_battle_cry(self):
        """Abstract method for battle cry - must be implemented by subclasses"""
        pass
    
    def _apply_type_stats(self):
        """Apply stats based on enemy type"""
        try:
            if self.enemy_type in Config.ENEMY_TYPES:
                stats = Config.ENEMY_TYPES[self.enemy_type]
                self.max_health = stats["health"]
                self.current_health = self.max_health
                self.attack = stats["attack"]
                self.behavior_pattern = stats["behavior"]
                
                # Adjust limb health based on enemy size
                limb_multiplier = self.max_health / 50  # Base 50 health
                for limb in self.limbs.values():
                    limb["max_health"] = int(limb["max_health"] * limb_multiplier)
                    limb["health"] = limb["max_health"]
            
            # Boss enemies
            elif self.enemy_type in Config.BOSS_ENEMIES:
                stats = Config.BOSS_ENEMIES[self.enemy_type]
                self.max_health = stats["health"]
                self.current_health = self.max_health
                self.attack = stats["attack"]
                self.behavior_pattern = "boss"
                self.gold_reward = 100
                self.xp_reward = 75
                
                # Bosses have stronger limbs
                for limb in self.limbs.values():
                    limb["max_health"] = int(limb["max_health"] * 2)
                    limb["health"] = limb["max_health"]
                
                # Add boss-specific abilities
                self._add_boss_abilities()
                
        except Exception as e:
            print(f"Error applying enemy type stats: {e}")
    
    def _add_boss_abilities(self):
        """Add special abilities for boss enemies"""
        try:
            if self.name == "Metal Alice":
                self.special_abilities = ["Cyber Blast", "System Repair", "Data Corruption"]
            elif self.name == "Black Knight":
                self.special_abilities = ["Dark Strike", "Shadow Shield", "Nightmare Wave"]
            elif self.name == "Emperor Mavro":
                self.special_abilities = ["Imperial Blast", "Royal Guard", "Conquest Beam"]
        except Exception as e:
            print(f"Error adding boss abilities: {e}")
    
    def update_ai_state(self):
        """Update AI state based on health and conditions"""
        try:
            health_percentage = self.current_health / self.max_health
            
            # State transitions based on health
            if health_percentage <= 0.2:
                if random.random() < 0.6:  # 60% chance to flee when very low health
                    self.state = EnemyState.FLEEING
                else:
                    self.state = EnemyState.ENRAGED  # Last stand
            elif health_percentage <= 0.4:
                if self.behavior_pattern == "defensive":
                    self.state = EnemyState.DEFENSIVE
                else:
                    self.state = EnemyState.AGGRESSIVE
            else:
                if self.behavior_pattern == "aggressive":
                    self.state = EnemyState.AGGRESSIVE
                elif self.behavior_pattern == "defensive":
                    self.state = EnemyState.DEFENSIVE
                else:
                    self.state = random.choice([EnemyState.AGGRESSIVE, EnemyState.DEFENSIVE])
            
            # Check for broken limbs affecting state
            broken_limbs = sum(1 for limb in self.limbs.values() if limb["broken"])
            if broken_limbs >= 2:
                self.state = EnemyState.DEFENSIVE
            
        except Exception as e:
            print(f"Error updating AI state: {e}")
    
    def choose_action(self, player):
        """Choose action based on AI state and behavior"""
        try:
            self.turn_counter += 1
            self.update_ai_state()
            
            # Remove expired status effects
            self.status_effects = [effect for effect in self.status_effects 
                                 if effect.get("duration", 0) > 0]
            for effect in self.status_effects:
                effect["duration"] -= 1
            
            # Check if stunned
            if any(effect["type"] == "stunned" for effect in self.status_effects):
                return "stunned", "The enemy is stunned and cannot act!"
            
            # State-based actions
            if self.state == EnemyState.FLEEING:
                if random.random() < 0.3:  # 30% chance to successfully flee
                    return "flee", f"{self.name} attempts to flee!"
                else:
                    return "desperate_attack", f"{self.name} makes a desperate attack!"
            
            elif self.state == EnemyState.ENRAGED:
                return "enraged_attack", f"{self.name} is enraged and attacks with fury!"
            
            elif self.state == EnemyState.DEFENSIVE:
                if random.random() < 0.4:
                    return "defend", f"{self.name} takes a defensive stance!"
                else:
                    return "heal", f"{self.name} tries to recover!"
            
            else:  # AGGRESSIVE or default
                # Choose attack type
                actions = ["basic_attack"]
                
                if self.special_abilities and random.random() < 0.3:
                    actions.append("special_attack")
                
                if self.turn_counter % 3 == 0:  # Every 3 turns, chance for power attack
                    actions.append("power_attack")
                
                action = random.choice(actions)
                return action, f"{self.name} prepares to attack!"
                
        except Exception as e:
            print(f"Error choosing action: {e}")
            return "basic_attack", f"{self.name} attacks!"
    
    def execute_action(self, action, player):
        """Execute the chosen action"""
        try:
            damage_dealt = 0
            message = ""
            
            if action == "basic_attack":
                damage = self.calculate_attack_damage()
                damage_dealt = player.take_damage(damage)
                message = f"{self.name} attacks for {damage_dealt} damage!"
            
            elif action == "power_attack":
                damage = self.calculate_attack_damage() * 1.5
                damage_dealt = player.take_damage(damage)
                message = f"{self.name} uses a powerful attack for {damage_dealt} damage!"
            
            elif action == "enraged_attack":
                damage = self.calculate_attack_damage() * 2.0
                damage_dealt = player.take_damage(damage)
                message = f"{self.name}'s enraged attack deals {damage_dealt} massive damage!"
            
            elif action == "desperate_attack":
                damage = self.calculate_attack_damage() * 1.2
                damage_dealt = player.take_damage(damage)
                message = f"{self.name}'s desperate attack deals {damage_dealt} damage!"
            
            elif action == "special_attack":
                if self.special_abilities:
                    ability = random.choice(self.special_abilities)
                    damage, special_message = self.use_special_ability(ability, player)
                    damage_dealt = player.take_damage(damage)
                    message = f"{self.name} uses {ability}! {special_message} Deals {damage_dealt} damage!"
                else:
                    damage = self.calculate_attack_damage()
                    damage_dealt = player.take_damage(damage)
                    message = f"{self.name} attacks for {damage_dealt} damage!"
            
            elif action == "defend":
                self.defense += 5  # Temporary defense boost
                heal_amount = self.max_health * 0.1
                self.current_health = min(self.max_health, self.current_health + heal_amount)
                message = f"{self.name} defends and recovers {heal_amount:.0f} health!"
            
            elif action == "heal":
                heal_amount = self.max_health * 0.15
                self.current_health = min(self.max_health, self.current_health + heal_amount)
                message = f"{self.name} heals for {heal_amount:.0f} health!"
            
            elif action == "flee":
                message = f"{self.name} is trying to escape!"
            
            elif action == "stunned":
                message = f"{self.name} is stunned and cannot act!"
            
            return damage_dealt, message
            
        except Exception as e:
            print(f"Error executing action: {e}")
            return 0, f"{self.name} stumbles!"
    
    def use_special_ability(self, ability, player):
        """Use a special ability"""
        try:
            if ability == "Cyber Blast":
                return self.attack * 1.8, "Cyber energy surges!"
            elif ability == "System Repair":
                heal = self.max_health * 0.25
                self.current_health = min(self.max_health, self.current_health + heal)
                return 0, f"Systems repaired for {heal:.0f} health!"
            elif ability == "Data Corruption":
                player.status_effects.append({"type": "corrupted", "duration": 2})
                return self.attack * 1.2, "Your systems are corrupted!"
            elif ability == "Dark Strike":
                return self.attack * 2.0, "Darkness engulfs you!"
            elif ability == "Shadow Shield":
                self.defense += 10
                return 0, "Shadow armor activated!"
            elif ability == "Nightmare Wave":
                return self.attack * 1.5, "Nightmares cloud your mind!"
            elif ability == "Imperial Blast":
                return self.attack * 2.5, "Imperial power unleashed!"
            elif ability == "Royal Guard":
                self.defense += 15
                return 0, "Royal defenses raised!"
            elif ability == "Conquest Beam":
                return self.attack * 2.2, "Conquest beam fired!"
            else:
                return self.attack, "Special attack!"
                
        except Exception as e:
            print(f"Error using special ability: {e}")
            return self.attack, "Attack!"
    
    def calculate_attack_damage(self):
        """Calculate attack damage with limb penalties"""
        try:
            base_damage = self.attack
            
            # Apply limb damage penalties
            if self.limbs["left_arm"]["broken"] or self.limbs["right_arm"]["broken"]:
                base_damage *= 0.7  # 30% damage reduction with broken arms
            
            if self.limbs["left_leg"]["broken"] and self.limbs["right_leg"]["broken"]:
                base_damage *= 0.8  # 20% damage reduction with both legs broken
            
            # Add some randomness
            damage = base_damage * random.uniform(0.8, 1.2)
            
            return max(1, int(damage))
            
        except Exception as e:
            print(f"Error calculating attack damage: {e}")
            return self.attack
    
    def take_limb_damage(self, limb_name, damage):
        """Take damage to a specific limb"""
        try:
            if limb_name not in self.limbs:
                return False, "Invalid limb!"
            
            limb = self.limbs[limb_name]
            if limb["broken"]:
                return False, f"{limb_name} is already broken!"
            
            limb["health"] -= damage
            
            if limb["health"] <= 0:
                limb["health"] = 0
                limb["broken"] = True
                
                # Apply effects based on broken limb
                if "arm" in limb_name:
                    self.attack = int(self.attack * 0.8)  # Reduce attack
                    return True, f"{self.name}'s {limb_name} is broken! Attack power reduced!"
                elif "leg" in limb_name:
                    self.speed = int(self.speed * 0.8)  # Reduce speed
                    return True, f"{self.name}'s {limb_name} is broken! Speed reduced!"
            
            return True, f"{self.name}'s {limb_name} takes {damage} damage!"
            
        except Exception as e:
            print(f"Error taking limb damage: {e}")
            return False, "Error applying limb damage!"
    
    def take_damage(self, damage, damage_type="normal"):
        """Take damage with defense calculation"""
        try:
            # Apply defense
            actual_damage = max(1, damage - self.defense)
            
            self.current_health -= actual_damage
            self.current_health = max(0, self.current_health)
            
            # Reset temporary defense boost
            if hasattr(self, '_temp_defense_boost'):
                self.defense -= 5
                delattr(self, '_temp_defense_boost')
            
            # Chance for limb damage on critical hits
            if damage > self.attack * 1.5:  # Critical hit
                limb_names = list(self.limbs.keys())
                target_limb = random.choice(limb_names)
                limb_damage = damage // 3
                self.take_limb_damage(target_limb, limb_damage)
            
            return actual_damage
            
        except Exception as e:
            print(f"Error taking damage: {e}")
            return damage
    
    def is_alive(self):
        """Check if enemy is alive"""
        return self.current_health > 0
    
    def get_health_bar(self, width=20):
        """Get a visual health bar"""
        try:
            if self.max_health <= 0:
                return "[" + "?" * width + "]"
            
            health_ratio = self.current_health / self.max_health
            filled = int(width * health_ratio)
            empty = width - filled
            
            bar = "[" + "█" * filled + "░" * empty + "]"
            return f"{bar} {self.current_health}/{self.max_health}"
            
        except Exception as e:
            print(f"Error creating health bar: {e}")
            return f"[ERROR] {self.current_health}/{self.max_health}"
    
    def get_status_description(self):
        """Get description of enemy's current status"""
        try:
            descriptions = []
            
            # Health status
            health_ratio = self.current_health / self.max_health
            if health_ratio <= 0.2:
                descriptions.append("critically wounded")
            elif health_ratio <= 0.5:
                descriptions.append("badly injured")
            elif health_ratio <= 0.8:
                descriptions.append("wounded")
            
            # Limb status
            broken_limbs = [name for name, limb in self.limbs.items() if limb["broken"]]
            if broken_limbs:
                descriptions.append(f"broken {', '.join(broken_limbs)}")
            
            # AI state
            if self.state == EnemyState.ENRAGED:
                descriptions.append("enraged")
            elif self.state == EnemyState.FLEEING:
                descriptions.append("trying to flee")
            elif self.state == EnemyState.DEFENSIVE:
                descriptions.append("defensive")
            
            # Status effects
            for effect in self.status_effects:
                descriptions.append(effect["type"])
            
            if descriptions:
                return f"{self.name} is {', '.join(descriptions)}"
            else:
                return f"{self.name} appears ready for battle"
                
        except Exception as e:
            print(f"Error getting status description: {e}")
            return f"{self.name} status unknown"

# Concrete Enemy Subclasses demonstrating inheritance and polymorphism
class Loogies(Enemy):
    """Basic foot soldier enemy"""
    
    def __init__(self):
        super().__init__("Loogies", "Loogies")
        self.behavior_pattern = "aggressive"
    
    def get_special_attack(self):
        return "Swarm Strike", self.attack * 1.3
    
    def get_battle_cry(self):
        return "For the Armada!"

class Zombats(Enemy):
    """Flying bat-like enemies"""
    
    def __init__(self):
        super().__init__("Zombats", "Zombats")
        self.behavior_pattern = "swarm"
        self.speed += 5  # Faster due to flight
    
    def get_special_attack(self):
        return "Sonic Screech", self.attack * 1.4
    
    def get_battle_cry(self):
        return "Screeeech!"

class Bruisers(Enemy):
    """Heavy tank-like enemies"""
    
    def __init__(self):
        super().__init__("Bruisers", "Bruisers")
        self.behavior_pattern = "tank"
        self.defense += 3  # More defensive
    
    def get_special_attack(self):
        return "Ground Pound", self.attack * 1.6
    
    def get_battle_cry(self):
        return "Crush the Rangers!"

class XBorgs(Enemy):
    """Tactical robot enemies"""
    
    def __init__(self):
        super().__init__("X-Borgs", "X-Borgs")
        self.behavior_pattern = "tactical"
        self.attack += 2  # More precise
    
    def get_special_attack(self):
        return "Laser Barrage", self.attack * 1.5
    
    def get_battle_cry(self):
        return "Exterminate Rangers!"

# Boss Enemies with enhanced abilities
class MetalAlice(Enemy):
    """Robotic boss enemy"""
    
    def __init__(self):
        super().__init__("Metal Alice", "Metal Alice")
        self.behavior_pattern = "boss"
        self.phases = 2
        self.current_phase = 1
    
    def get_special_attack(self):
        if self.current_phase == 1:
            return "Cyber Blast", self.attack * 2.0
        else:
            return "System Override", self.attack * 2.5
    
    def get_battle_cry(self):
        return "I am the future of warfare!"
    
    def phase_transition(self):
        """Trigger phase transition at low health"""
        if self.current_health <= self.max_health * 0.5 and self.current_phase == 1:
            self.current_phase = 2
            self.attack = int(self.attack * 1.2)
            self.defense = int(self.defense * 1.1)
            return True, "Metal Alice enters Phase 2! Systems upgraded!"
        return False, ""

class BlackKnight(Enemy):
    """Dark warrior boss"""
    
    def __init__(self):
        super().__init__("Black Knight", "Black Knight")
        self.behavior_pattern = "boss"
        self.phases = 3
        self.current_phase = 1
    
    def get_special_attack(self):
        phase_attacks = {
            1: ("Dark Strike", self.attack * 1.8),
            2: ("Shadow Blade", self.attack * 2.2),
            3: ("Nightmare Slash", self.attack * 2.8)
        }
        return phase_attacks.get(self.current_phase, ("Dark Strike", self.attack * 1.8))
    
    def get_battle_cry(self):
        return "Darkness will consume all!"

class EmperorMavro(Enemy):
    """Final boss enemy"""
    
    def __init__(self):
        super().__init__("Emperor Mavro", "Emperor Mavro")
        self.behavior_pattern = "boss"
        self.phases = 3
        self.current_phase = 1
        self.royal_guard = True
    
    def get_special_attack(self):
        if self.royal_guard:
            return "Imperial Blast", self.attack * 2.5
        else:
            return "Conquest Beam", self.attack * 3.0
    
    def get_battle_cry(self):
        return "I am the Emperor of the universe!"

def create_enemy(enemy_type, mission_difficulty="Medium"):
    """Factory function to create enemies using polymorphism"""
    try:
        # Enemy class mapping
        enemy_classes = {
            "Loogies": Loogies,
            "Zombats": Zombats,
            "Bruisers": Bruisers,
            "X-Borgs": XBorgs,
            "Metal Alice": MetalAlice,
            "Black Knight": BlackKnight,
            "Emperor Mavro": EmperorMavro
        }
        
        if enemy_type == "random":
            enemy_type = random.choice(list(Config.ENEMY_TYPES.keys()))
        
        # Create enemy using appropriate class
        if enemy_type in enemy_classes:
            enemy = enemy_classes[enemy_type]()
        else:
            # Fallback to base Enemy class
            enemy = Loogies()  # Default to Loogies
        
        # Apply difficulty scaling
        difficulty_multipliers = {
            "Easy": 0.8,
            "Medium": 1.0,
            "Hard": 1.3,
            "Extreme": 1.6
        }
        
        multiplier = difficulty_multipliers.get(mission_difficulty, 1.0)
        
        enemy.max_health = int(enemy.max_health * multiplier)
        enemy.current_health = enemy.max_health
        enemy.attack = int(enemy.attack * multiplier)
        enemy.defense = int(enemy.defense * multiplier)
        enemy.gold_reward = int(enemy.gold_reward * multiplier)
        enemy.xp_reward = int(enemy.xp_reward * multiplier)
        
        return enemy
        
    except Exception as e:
        print(f"Error creating enemy: {e}")
        return Loogies()  # Safe fallback
