import random
from config import Config

class PowerRanger:
    def __init__(self, name="", color="", power_type="", weapon=""):
        # Basic Info
        self.name = name
        self.color = color
        self.power_type = power_type
        self.weapon = weapon
        
        # Stats
        self.level = 1
        self.xp = 0
        self.max_health = Config.BASE_HEALTH
        self.current_health = self.max_health
        self.attack = Config.BASE_ATTACK
        self.defense = Config.BASE_DEFENSE
        self.speed = Config.BASE_SPEED
        
        # Resources
        self.gold = 100
        self.mega_energy = 3
        self.skill_points = 0
        
        # Collections
        self.ranger_keys = []
        self.battle_history = []
        self.investments = {}
        
        # Skills
        self.skills = {
            "Power Strike": False,
            "Mega Blast": False,
            "Healing Light": False,
            "Speed Boost": False,
            "Medic Protocol": False
        }
        
        # Combat States
        self.limb_damage = {"arms": 0, "legs": 0}
        self.status_effects = []
        
        # Apply bonuses if character is created
        if color and power_type and weapon:
            self._apply_creation_bonuses()
    
    def _apply_creation_bonuses(self):
        """Apply bonuses based on character creation choices"""
        try:
            # Color bonuses
            if self.color in Config.COLOR_BONUSES:
                bonuses = Config.COLOR_BONUSES[self.color]
                self.max_health += bonuses.get("health", 0)
                self.attack += bonuses.get("attack", 0)
                self.defense += bonuses.get("defense", 0)
                self.speed += bonuses.get("speed", 0)
                self.current_health = self.max_health
            
            # Power type bonuses
            if self.power_type in Config.POWER_BONUSES:
                bonuses = Config.POWER_BONUSES[self.power_type]
                self.attack += bonuses.get("attack", 0)
                self.defense += bonuses.get("defense", 0)
                self.speed += bonuses.get("speed", 0)
            
            # Weapon bonuses
            if self.weapon in Config.WEAPON_STATS:
                weapon_stats = Config.WEAPON_STATS[self.weapon]
                self.attack += weapon_stats.get("damage", 0)
                self.speed += weapon_stats.get("speed", 0)  # Can be negative
                
        except Exception as e:
            print(f"Error applying creation bonuses: {e}")
    
    def get_health_bar(self, width=20):
        """Get a visual health bar for the player"""
        try:
            if self.max_health <= 0:
                return "[" + "?" * width + "]"
            
            health_ratio = self.current_health / self.max_health
            filled = int(width * health_ratio)
            empty = width - filled
            
            # Use different characters for player health bar
            if health_ratio > 0.6:
                fill_char = "█"  # Full health - solid
            elif health_ratio > 0.3:
                fill_char = "▓"  # Medium health - medium
            else:
                fill_char = "▒"  # Low health - light
            
            bar = "[" + fill_char * filled + "░" * empty + "]"
            return f"{bar} {self.current_health:.0f}/{self.max_health}"
            
        except Exception as e:
            print(f"Error creating health bar: {e}")
            return f"[ERROR] {self.current_health:.0f}/{self.max_health}"
    
    def gain_xp(self, amount):
        """Gain XP and level up if needed"""
        try:
            self.xp += amount
            old_level = self.level
            
            while self.xp >= Config.XP_PER_LEVEL * self.level and self.level < Config.MAX_LEVEL:
                self.level += 1
                self.skill_points += 1
                
                # Stat increases on level up
                health_increase = Config.LEVEL_STAT_BONUS
                self.max_health += health_increase
                self.current_health += health_increase
                self.attack += 2
                self.defense += 1
                self.speed += 1
                
                print(f"🎉 LEVEL UP! You are now level {self.level}!")
                print(f"💪 Stats increased: +{health_increase} Health, +2 Attack, +1 Defense, +1 Speed")
                print(f"⭐ You gained 1 skill point!")
                
                # Unlock skills at certain levels
                if self.level == 3 and not self.skills["Power Strike"]:
                    self.skills["Power Strike"] = True
                    print("🔓 New skill unlocked: Power Strike!")
                elif self.level == 5 and not self.skills["Mega Blast"]:
                    self.skills["Mega Blast"] = True
                    print("🔓 New skill unlocked: Mega Blast!")
                elif self.level == 7 and not self.skills["Healing Light"]:
                    self.skills["Healing Light"] = True
                    print("🔓 New skill unlocked: Healing Light!")
                
            return self.level > old_level
            
        except Exception as e:
            print(f"Error gaining XP: {e}")
            return False
    
    def learn_skill(self, skill_name):
        """Learn a new skill using skill points"""
        try:
            if skill_name not in self.skills:
                return False, "Unknown skill!"
            
            if self.skills[skill_name]:
                return False, "Skill already learned!"
            
            if self.skill_points <= 0:
                return False, "Not enough skill points!"
            
            self.skills[skill_name] = True
            self.skill_points -= 1
            return True, f"Learned {skill_name}!"
            
        except Exception as e:
            print(f"Error learning skill: {e}")
            return False, "Error learning skill!"
    
    def use_skill(self, skill_name, target=None):
        """Use a learned skill"""
        try:
            if skill_name not in self.skills or not self.skills[skill_name]:
                return False, "Skill not available!"
            
            if skill_name == "Power Strike":
                if self.mega_energy >= 1:
                    self.mega_energy -= 1
                    damage = self.attack * 1.5
                    return True, f"Power Strike deals {damage:.0f} damage!"
                else:
                    return False, "Not enough Mega Energy!"
            
            elif skill_name == "Mega Blast":
                if self.mega_energy >= 2:
                    self.mega_energy -= 2
                    damage = self.attack * 2.0
                    return True, f"Mega Blast deals {damage:.0f} damage!"
                else:
                    return False, "Not enough Mega Energy!"
            
            elif skill_name == "Healing Light":
                if self.mega_energy >= 1:
                    self.mega_energy -= 1
                    heal_amount = self.max_health * 0.3
                    self.current_health = min(self.max_health, self.current_health + heal_amount)
                    return True, f"Healed {heal_amount:.0f} health!"
                else:
                    return False, "Not enough Mega Energy!"
            
            elif skill_name == "Speed Boost":
                if self.mega_energy >= 1:
                    self.mega_energy -= 1
                    self.status_effects.append({"type": "speed_boost", "duration": 3})
                    return True, "Speed increased for 3 turns!"
                else:
                    return False, "Not enough Mega Energy!"
            
            elif skill_name == "Medic Protocol":
                if self.mega_energy >= 2:
                    self.mega_energy -= 2
                    heal_amount = self.max_health * 0.5
                    self.current_health = min(self.max_health, self.current_health + heal_amount)
                    # Clear limb damage
                    self.limb_damage = {"arms": 0, "legs": 0}
                    return True, f"Full healing protocol activated! Healed {heal_amount:.0f} health and cleared limb damage!"
                else:
                    return False, "Not enough Mega Energy!"
            
            return False, "Unknown skill effect!"
            
        except Exception as e:
            print(f"Error using skill: {e}")
            return False, "Error using skill!"
    
    def add_ranger_key(self, key_name):
        """Add a Ranger Key to collection"""
        try:
            if key_name not in self.ranger_keys:
                self.ranger_keys.append(key_name)
                print(f"🔑 Legendary Ranger Key acquired: {key_name}!")
                
                # Bonus for collecting keys
                if len(self.ranger_keys) % 5 == 0:
                    self.mega_energy += 1
                    print(f"🌟 Mega Energy bonus! You now have {self.mega_energy} Mega Energy!")
                
                return True
            return False
            
        except Exception as e:
            print(f"Error adding Ranger Key: {e}")
            return False
    
    def can_use_fusion_power(self):
        """Check if fusion power can be used"""
        return self.level >= 3 and self.mega_energy >= 3 and len(self.ranger_keys) >= 2
    
    def use_fusion_power(self):
        """Use fusion power for massive damage"""
        try:
            if not self.can_use_fusion_power():
                return False, "Cannot use Fusion Power! Need level 3+, 3 Mega Energy, and 2+ Ranger Keys!"
            
            self.mega_energy -= 3
            damage = self.attack * 3.0
            return True, f"🌟 FUSION POWER ACTIVATED! Deals {damage:.0f} massive damage!"
            
        except Exception as e:
            print(f"Error using fusion power: {e}")
            return False, "Error using fusion power!"
    
    def take_damage(self, damage, damage_type="normal"):
        """Take damage with defense calculation"""
        try:
            # Apply defense
            actual_damage = max(1, damage - self.defense)
            
            # Apply limb damage penalties
            if self.limb_damage["arms"] > 0:
                actual_damage *= 1.2  # Take more damage with injured arms
            
            self.current_health -= actual_damage
            self.current_health = max(0, self.current_health)
            
            return actual_damage
            
        except Exception as e:
            print(f"Error taking damage: {e}")
            return damage
    
    def heal(self, amount):
        """Heal the character"""
        try:
            old_health = self.current_health
            self.current_health = min(self.max_health, self.current_health + amount)
            actual_heal = self.current_health - old_health
            return actual_heal
            
        except Exception as e:
            print(f"Error healing: {e}")
            return 0
    
    def is_alive(self):
        """Check if character is alive"""
        return self.current_health > 0
    
    def get_stats_dict(self):
        """Get character stats as dictionary for saving"""
        try:
            return {
                "name": self.name,
                "color": self.color,
                "power_type": self.power_type,
                "weapon": self.weapon,
                "level": self.level,
                "xp": self.xp,
                "max_health": self.max_health,
                "current_health": self.current_health,
                "attack": self.attack,
                "defense": self.defense,
                "speed": self.speed,
                "gold": self.gold,
                "mega_energy": self.mega_energy,
                "skill_points": self.skill_points,
                "ranger_keys": self.ranger_keys,
                "battle_history": self.battle_history,
                "investments": self.investments,
                "skills": self.skills,
                "limb_damage": self.limb_damage,
                "status_effects": self.status_effects
            }
        except Exception as e:
            print(f"Error getting stats dict: {e}")
            return {}
    
    def load_from_dict(self, data):
        """Load character from dictionary"""
        try:
            self.name = data.get("name", "")
            self.color = data.get("color", "")
            self.power_type = data.get("power_type", "")
            self.weapon = data.get("weapon", "")
            self.level = data.get("level", 1)
            self.xp = data.get("xp", 0)
            self.max_health = data.get("max_health", Config.BASE_HEALTH)
            self.current_health = data.get("current_health", self.max_health)
            self.attack = data.get("attack", Config.BASE_ATTACK)
            self.defense = data.get("defense", Config.BASE_DEFENSE)
            self.speed = data.get("speed", Config.BASE_SPEED)
            self.gold = data.get("gold", 100)
            self.mega_energy = data.get("mega_energy", 3)
            self.skill_points = data.get("skill_points", 0)
            self.ranger_keys = data.get("ranger_keys", [])
            self.battle_history = data.get("battle_history", [])
            self.investments = data.get("investments", {})
            self.skills = data.get("skills", {
                "Power Strike": False,
                "Mega Blast": False,
                "Healing Light": False,
                "Speed Boost": False,
                "Medic Protocol": False
            })
            self.limb_damage = data.get("limb_damage", {"arms": 0, "legs": 0})
            self.status_effects = data.get("status_effects", [])
            
            return True
            
        except Exception as e:
            print(f"Error loading character data: {e}")
            return False
    
    def show_character_sheet(self):
        """Display detailed character information"""
        try:
            print(f"\n📋 CHARACTER SHEET - {self.name}")
            print("=" * 40)
            print(f"🎨 Color: {self.color} Ranger")
            print(f"⚡ Power Type: {self.power_type}")
            print(f"⚔️ Weapon: {self.weapon}")
            print(f"📊 Level: {self.level} (XP: {self.xp}/{Config.XP_PER_LEVEL * self.level})")
            
            print(f"\n💪 STATS:")
            print(f"❤️ Health: {self.get_health_bar()}")
            print(f"⚔️ Attack: {self.attack}")
            print(f"🛡️ Defense: {self.defense}")
            print(f"💨 Speed: {self.speed}")
            
            print(f"\n💰 RESOURCES:")
            print(f"🪙 Gold: {self.gold}")
            print(f"⚡ Mega Energy: {self.mega_energy}")
            print(f"⭐ Skill Points: {self.skill_points}")
            
            print(f"\n🔑 RANGER KEYS ({len(self.ranger_keys)}):")
            if self.ranger_keys:
                for key in self.ranger_keys:
                    print(f"  • {key}")
            else:
                print("  None collected yet")
            
            print(f"\n🎯 SKILLS:")
            for skill, learned in self.skills.items():
                status = "✅" if learned else "❌"
                print(f"  {status} {skill}")
            
            if self.limb_damage["arms"] > 0 or self.limb_damage["legs"] > 0:
                print(f"\n🩹 INJURIES:")
                if self.limb_damage["arms"] > 0:
                    print(f"  💪 Arm damage: {self.limb_damage['arms']}")
                if self.limb_damage["legs"] > 0:
                    print(f"  🦵 Leg damage: {self.limb_damage['legs']}")
            
            if self.status_effects:
                print(f"\n✨ STATUS EFFECTS:")
                for effect in self.status_effects:
                    print(f"  • {effect['type']} ({effect['duration']} turns)")
            
            if self.can_use_fusion_power():
                print(f"\n🌟 FUSION POWER AVAILABLE!")
            
        except Exception as e:
            print(f"Error showing character sheet: {e}")
