import random
import time
from config import Config
from enemy import create_enemy
from battle import BattleSystem

class Mission:
    def __init__(self, mission_type, difficulty="Medium"):
        self.mission_type = mission_type
        self.difficulty = difficulty
        self.environment = self._get_environment()
        self.objectives = self._generate_objectives()
        self.rewards = self._calculate_rewards()
        self.time_limit = self._get_time_limit()
        self.completed = False
        
    def _get_environment(self):
        """Get environment based on mission type"""
        environment_map = {
            "City Defense": "City",
            "Forest Battle": "Forest",
            "Space Base": "Space Base",
            "Underwater": "Underwater",
            "Mountain Peak": "Mountain"
        }
        return environment_map.get(self.mission_type, "City")
    
    def _generate_objectives(self):
        """Generate mission objectives"""
        if self.mission_type == "City Defense":
            return {
                "type": "survival",
                "waves": 3,
                "enemies_per_wave": 2,
                "description": "Defend the city from monster waves"
            }
        elif self.mission_type == "Forest Battle":
            return {
                "type": "elimination",
                "target_count": 4,
                "description": "Clear the forest of all monsters"
            }
        elif self.mission_type == "Space Base":
            return {
                "type": "boss",
                "boss_type": random.choice(list(Config.BOSS_ENEMIES.keys())),
                "description": "Defeat the boss in their stronghold"
            }
        elif self.mission_type == "Underwater":
            return {
                "type": "escort",
                "escort_health": 100,
                "waves": 2,
                "description": "Escort civilians to safety"
            }
        elif self.mission_type == "Mountain Peak":
            return {
                "type": "timed_survival",
                "duration": 5,  # turns
                "description": "Survive the mountain assault"
            }
        else:
            return {
                "type": "basic",
                "description": "Complete the mission"
            }
    
    def _calculate_rewards(self):
        """Calculate mission rewards based on type and difficulty"""
        base_rewards = {
            "Easy": {"gold": 50, "xp": 30},
            "Medium": {"gold": 100, "xp": 60},
            "Hard": {"gold": 200, "xp": 120},
            "Extreme": {"gold": 400, "xp": 250}
        }
        
        base = base_rewards.get(self.difficulty, base_rewards["Medium"])
        
        # Mission type multipliers
        type_multipliers = {
            "City Defense": 1.2,
            "Forest Battle": 1.0,
            "Space Base": 1.5,
            "Underwater": 1.3,
            "Mountain Peak": 1.4
        }
        
        multiplier = type_multipliers.get(self.mission_type, 1.0)
        
        return {
            "gold": int(base["gold"] * multiplier),
            "xp": int(base["xp"] * multiplier),
            "ranger_key_chance": 0.4 if self.difficulty in ["Hard", "Extreme"] else 0.2
        }
    
    def _get_time_limit(self):
        """Get time limit for timed missions"""
        if self.objectives.get("type") == "timed_survival":
            return self.objectives.get("duration", 5)
        return None

class MissionSystem:
    def __init__(self):
        self.available_missions = []
        self.completed_missions = []
        self.current_mission = None
        self.battle_system = BattleSystem()
        
    def generate_missions(self):
        """Generate random available missions"""
        try:
            self.available_missions = []
            
            # Generate 3-5 random missions
            for _ in range(random.randint(3, 5)):
                mission_type = random.choice(Config.MISSION_TYPES)
                difficulty = random.choice(Config.MISSION_DIFFICULTIES)
                
                # Bias towards easier missions early on
                if len(self.completed_missions) < 3:
                    difficulty = random.choice(["Easy", "Medium"])
                
                mission = Mission(mission_type, difficulty)
                self.available_missions.append(mission)
                
        except Exception as e:
            print(f"Error generating missions: {e}")
    
    def show_available_missions(self):
        """Display available missions"""
        try:
            if not self.available_missions:
                self.generate_missions()
            
            print(f"\n🎯 AVAILABLE MISSIONS")
            print("=" * 40)
            
            for i, mission in enumerate(self.available_missions, 1):
                print(f"{i}. {mission.mission_type} ({mission.difficulty})")
                print(f"   📍 {mission.environment}")
                print(f"   📋 {mission.objectives['description']}")
                print(f"   💰 Rewards: {mission.rewards['gold']} gold, {mission.rewards['xp']} XP")
                if mission.time_limit:
                    print(f"   ⏰ Time Limit: {mission.time_limit} turns")
                print()
            
            print(f"{len(self.available_missions) + 1}. Return to main menu")
            
        except Exception as e:
            print(f"Error showing missions: {e}")
    
    def select_mission(self, player):
        """Let player select and start a mission"""
        try:
            self.show_available_missions()
            
            choice = input(f"\nSelect mission (1-{len(self.available_missions) + 1}): ").strip()
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(self.available_missions):
                    selected_mission = self.available_missions[choice_num - 1]
                    return self.start_mission(player, selected_mission)
                elif choice_num == len(self.available_missions) + 1:
                    return None
                else:
                    print("❌ Invalid choice!")
                    return self.select_mission(player)
            except ValueError:
                print("❌ Please enter a number!")
                return self.select_mission(player)
                
        except Exception as e:
            print(f"Error selecting mission: {e}")
            return None
    
    def start_mission(self, player, mission):
        """Start the selected mission"""
        try:
            self.current_mission = mission
            
            print(f"\n🚀 MISSION START: {mission.mission_type}")
            print("=" * 50)
            print(f"📍 Location: {mission.environment}")
            print(f"🎯 Objective: {mission.objectives['description']}")
            print(f"⚠️ Difficulty: {mission.difficulty}")
            if mission.time_limit:
                print(f"⏰ Time Limit: {mission.time_limit} turns")
            print("=" * 50)
            
            input("Press Enter to begin mission...")
            
            # Execute mission based on type
            result = self._execute_mission(player, mission)
            
            # Handle mission completion
            if result["success"]:
                self._handle_mission_success(player, mission, result)
                self.completed_missions.append(mission)
                if mission in self.available_missions:
                    self.available_missions.remove(mission)
            else:
                self._handle_mission_failure(player, mission, result)
            
            self.current_mission = None
            return result
            
        except Exception as e:
            print(f"Error starting mission: {e}")
            return {"success": False, "message": "Mission system error"}
    
    def _execute_mission(self, player, mission):
        """Execute mission based on its type"""
        try:
            obj_type = mission.objectives["type"]
            
            if obj_type == "survival":
                return self._execute_survival_mission(player, mission)
            elif obj_type == "elimination":
                return self._execute_elimination_mission(player, mission)
            elif obj_type == "boss":
                return self._execute_boss_mission(player, mission)
            elif obj_type == "escort":
                return self._execute_escort_mission(player, mission)
            elif obj_type == "timed_survival":
                return self._execute_timed_survival_mission(player, mission)
            else:
                return self._execute_basic_mission(player, mission)
                
        except Exception as e:
            print(f"Error executing mission: {e}")
            return {"success": False, "message": "Mission execution error"}
    
    def _execute_survival_mission(self, player, mission):
        """Execute survival mission with waves of enemies"""
        try:
            waves = mission.objectives["waves"]
            enemies_per_wave = mission.objectives["enemies_per_wave"]
            
            for wave in range(1, waves + 1):
                print(f"\n🌊 WAVE {wave}/{waves}")
                print("=" * 30)
                
                # Create enemies for this wave
                wave_enemies = []
                for _ in range(enemies_per_wave):
                    enemy = create_enemy("random", mission.difficulty)
                    wave_enemies.append(enemy)
                
                # Battle each enemy
                for i, enemy in enumerate(wave_enemies, 1):
                    print(f"\n👹 Enemy {i}/{len(wave_enemies)}: {enemy.name}")
                    
                    battle_result = self.battle_system.start_battle(player, enemy, mission.environment)
                    
                    if battle_result["result"] == "defeat":
                        return {"success": False, "message": f"Defeated in wave {wave}"}
                    elif battle_result["result"] == "fled":
                        return {"success": False, "message": "Mission abandoned"}
                    
                    if not player.is_alive():
                        return {"success": False, "message": f"Defeated in wave {wave}"}
                
                if wave < waves:
                    print(f"\n✅ Wave {wave} complete!")
                    # Heal player between waves
                    heal_amount = player.max_health * 0.2
                    player.heal(heal_amount)
                    print(f"❤️ Healed {heal_amount:.0f} health between waves")
                    input("Press Enter for next wave...")
            
            return {"success": True, "message": f"All {waves} waves survived!"}
            
        except Exception as e:
            print(f"Error in survival mission: {e}")
            return {"success": False, "message": "Survival mission error"}
    
    def _execute_elimination_mission(self, player, mission):
        """Execute elimination mission"""
        try:
            target_count = mission.objectives["target_count"]
            defeated_count = 0
            
            print(f"🎯 Eliminate {target_count} enemies!")
            
            while defeated_count < target_count:
                enemy = create_enemy("random", mission.difficulty)
                print(f"\n👹 Enemy {defeated_count + 1}/{target_count}: {enemy.name}")
                
                battle_result = self.battle_system.start_battle(player, enemy, mission.environment)
                
                if battle_result["result"] == "victory":
                    defeated_count += 1
                    print(f"✅ Progress: {defeated_count}/{target_count}")
                elif battle_result["result"] == "defeat":
                    return {"success": False, "message": f"Defeated after eliminating {defeated_count} enemies"}
                elif battle_result["result"] == "fled":
                    print("⚠️ Enemy escaped, but mission continues...")
                
                if not player.is_alive():
                    return {"success": False, "message": f"Defeated after eliminating {defeated_count} enemies"}
                
                # Small heal between fights
                if defeated_count < target_count:
                    heal_amount = player.max_health * 0.1
                    player.heal(heal_amount)
                    print(f"❤️ Recovered {heal_amount:.0f} health")
            
            return {"success": True, "message": f"All {target_count} enemies eliminated!"}
            
        except Exception as e:
            print(f"Error in elimination mission: {e}")
            return {"success": False, "message": "Elimination mission error"}
    
    def _execute_boss_mission(self, player, mission):
        """Execute boss battle mission"""
        try:
            boss_type = mission.objectives["boss_type"]
            boss = create_enemy(boss_type, mission.difficulty)
            
            print(f"💀 BOSS BATTLE: {boss.name}")
            print("This will be a challenging fight!")
            
            # Give player a pre-battle boost
            player.mega_energy = min(5, player.mega_energy + 2)
            print(f"⚡ Pre-battle boost: +2 Mega Energy!")
            
            battle_result = self.battle_system.start_battle(player, boss, mission.environment)
            
            if battle_result["result"] == "victory":
                return {"success": True, "message": f"Boss {boss.name} defeated!", "boss_defeated": True}
            elif battle_result["result"] == "defeat":
                return {"success": False, "message": f"Defeated by boss {boss.name}"}
            else:
                return {"success": False, "message": "Boss battle abandoned"}
                
        except Exception as e:
            print(f"Error in boss mission: {e}")
            return {"success": False, "message": "Boss mission error"}
    
    def _execute_escort_mission(self, player, mission):
        """Execute escort mission"""
        try:
            escort_health = mission.objectives["escort_health"]
            waves = mission.objectives["waves"]
            current_escort_health = escort_health
            
            print(f"🚶 Escort Mission: Protect civilians ({escort_health} HP)")
            
            for wave in range(1, waves + 1):
                print(f"\n🌊 Assault Wave {wave}/{waves}")
                
                # Create enemies that target both player and escort
                enemies = []
                for _ in range(random.randint(1, 3)):
                    enemy = create_enemy("random", mission.difficulty)
                    enemies.append(enemy)
                
                for enemy in enemies:
                    print(f"\n👹 {enemy.name} attacks!")
                    
                    # Enemy chooses target (70% player, 30% escort)
                    if random.random() < 0.7:
                        # Attack player
                        battle_result = self.battle_system.start_battle(player, enemy, mission.environment)
                        
                        if battle_result["result"] == "defeat":
                            return {"success": False, "message": "You were defeated during escort"}
                        elif battle_result["result"] == "fled":
                            # If player flees, escort takes damage
                            escort_damage = enemy.attack
                            current_escort_health -= escort_damage
                            print(f"💔 Escort takes {escort_damage} damage while you flee!")
                    else:
                        # Attack escort directly
                        escort_damage = enemy.attack + random.randint(-5, 5)
                        current_escort_health -= escort_damage
                        print(f"💔 {enemy.name} attacks the escort for {escort_damage} damage!")
                        
                        # Player can intervene
                        choice = input("Intervene? (y/n): ").strip().lower()
                        if choice == 'y':
                            # Quick battle
                            player_damage = player.attack + random.randint(-3, 5)
                            enemy.take_damage(player_damage)
                            print(f"⚔️ You intervene and deal {player_damage} damage!")
                            
                            if enemy.is_alive():
                                counter_damage = enemy.attack // 2
                                player.take_damage(counter_damage)
                                print(f"💥 Enemy counters for {counter_damage} damage!")
                    
                    # Check escort health
                    if current_escort_health <= 0:
                        return {"success": False, "message": "Escort was defeated!"}
                
                print(f"❤️ Escort Health: {current_escort_health}/{escort_health}")
                
                if wave < waves:
                    input("Press Enter for next wave...")
            
            return {"success": True, "message": f"Escort mission complete! Escort survived with {current_escort_health} HP"}
            
        except Exception as e:
            print(f"Error in escort mission: {e}")
            return {"success": False, "message": "Escort mission error"}
    
    def _execute_timed_survival_mission(self, player, mission):
        """Execute timed survival mission"""
        try:
            duration = mission.objectives["duration"]
            turns_survived = 0
            
            print(f"⏰ Survive for {duration} turns!")
            
            while turns_survived < duration:
                turns_survived += 1
                print(f"\n⏰ Turn {turns_survived}/{duration}")
                
                # Random enemy appears
                enemy = create_enemy("random", mission.difficulty)
                print(f"👹 {enemy.name} appears!")
                
                # Player can choose to fight or evade
                choice = input("Fight (f) or Evade (e)? ").strip().lower()
                
                if choice == 'f':
                    battle_result = self.battle_system.start_battle(player, enemy, mission.environment)
                    
                    if battle_result["result"] == "defeat":
                        return {"success": False, "message": f"Defeated on turn {turns_survived}"}
                    elif battle_result["result"] == "victory":
                        print("✅ Enemy defeated!")
                elif choice == 'e':
                    # Evasion attempt
                    if random.random() < 0.7:  # 70% success rate
                        print("💨 Successfully evaded!")
                    else:
                        damage = enemy.attack // 2
                        player.take_damage(damage)
                        print(f"💥 Failed to evade! Took {damage} damage!")
                        
                        if not player.is_alive():
                            return {"success": False, "message": f"Defeated while evading on turn {turns_survived}"}
                else:
                    print("❌ Invalid choice, defaulting to fight!")
                    battle_result = self.battle_system.start_battle(player, enemy, mission.environment)
                    
                    if battle_result["result"] == "defeat":
                        return {"success": False, "message": f"Defeated on turn {turns_survived}"}
                
                if turns_survived < duration:
                    input("Press Enter for next turn...")
            
            return {"success": True, "message": f"Survived all {duration} turns!"}
            
        except Exception as e:
            print(f"Error in timed survival mission: {e}")
            return {"success": False, "message": "Timed survival mission error"}
    
    def _execute_basic_mission(self, player, mission):
        """Execute basic mission (single enemy)"""
        try:
            enemy = create_enemy("random", mission.difficulty)
            
            battle_result = self.battle_system.start_battle(player, enemy, mission.environment)
            
            if battle_result["result"] == "victory":
                return {"success": True, "message": "Mission completed!"}
            elif battle_result["result"] == "defeat":
                return {"success": False, "message": "Mission failed!"}
            else:
                return {"success": False, "message": "Mission abandoned!"}
                
        except Exception as e:
            print(f"Error in basic mission: {e}")
            return {"success": False, "message": "Basic mission error"}
    
    def _handle_mission_success(self, player, mission, result):
        """Handle successful mission completion"""
        try:
            print(f"\n🎉 MISSION COMPLETE!")
            print("=" * 30)
            
            # Base rewards
            gold_reward = mission.rewards["gold"]
            xp_reward = mission.rewards["xp"]
            
            # Bonus for boss missions
            if result.get("boss_defeated"):
                gold_reward = int(gold_reward * 1.5)
                xp_reward = int(xp_reward * 1.5)
                print("👑 Boss Bonus: +50% rewards!")
            
            # Apply rewards
            player.gold += gold_reward
            player.gain_xp(xp_reward)
            
            print(f"💰 Gold earned: {gold_reward}")
            print(f"⭐ XP earned: {xp_reward}")
            
            # Chance for Ranger Key
            if random.random() < mission.rewards["ranger_key_chance"]:
                ranger_keys = [
                    "Legendary Red Key", "Legendary Blue Key", "Legendary Yellow Key",
                    "Legendary Pink Key", "Legendary Black Key", "Legendary Green Key",
                    "Ancient Ranger Key", "Mystic Ranger Key", "Quantum Ranger Key"
                ]
                key = random.choice(ranger_keys)
                if player.add_ranger_key(key):
                    print(f"🔑 Mission Bonus: Found {key}!")
            
            # Special mission rewards
            if mission.difficulty == "Extreme":
                player.mega_energy = min(5, player.mega_energy + 1)
                print("⚡ Extreme Mission Bonus: +1 Mega Energy!")
            
        except Exception as e:
            print(f"Error handling mission success: {e}")
    
    def _handle_mission_failure(self, player, mission, result):
        """Handle mission failure"""
        try:
            print(f"\n💀 MISSION FAILED!")
            print("=" * 25)
            print(result["message"])
            
            # Small consolation reward
            consolation_gold = mission.rewards["gold"] // 4
            if consolation_gold > 0:
                player.gold += consolation_gold
                print(f"💰 Consolation reward: {consolation_gold} gold")
            
        except Exception as e:
            print(f"Error handling mission failure: {e}")
    
    def show_mission_history(self, player):
        """Show completed missions"""
        try:
            print(f"\n📜 MISSION HISTORY")
            print("=" * 30)
            
            if not self.completed_missions:
                print("📭 No missions completed yet!")
                return
            
            for i, mission in enumerate(self.completed_missions, 1):
                print(f"{i}. {mission.mission_type} ({mission.difficulty})")
                print(f"   📍 {mission.environment}")
                print(f"   ✅ Completed")
                print()
            
            print(f"Total missions completed: {len(self.completed_missions)}")
            
        except Exception as e:
            print(f"Error showing mission history: {e}")
