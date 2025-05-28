import random
import time
from config import Config
from enemy import Enemy, EnemyState

class BattleSystem:
    def __init__(self):
        self.battle_log = []
        self.turn_counter = 0
        self.combo_active = False
        self.combo_sequence = []
        self.combo_timer = 0
        
    def start_battle(self, player, enemy, environment="City"):
        """Start a battle between player and enemy"""
        try:
            self.battle_log = []
            self.turn_counter = 0
            self.combo_active = False
            
            print(f"\n⚔️ BATTLE START!")
            print("=" * 40)
            print(f"🦸 {player.name} ({player.color} Ranger)")
            print(f"👹 {enemy.name}")
            print(f"🌍 Environment: {environment}")
            print("=" * 40)
            
            # Apply environment effects
            self._apply_environment_effects(player, enemy, environment)
            
            battle_result = self._battle_loop(player, enemy, environment)
            
            return battle_result
            
        except Exception as e:
            print(f"Error starting battle: {e}")
            return {"result": "error", "message": "Battle system error"}
    
    def _apply_environment_effects(self, player, enemy, environment):
        """Apply environmental effects to battle"""
        try:
            if environment == "Forest":
                player.speed += 3  # Agility bonus in forest
                print("🌲 Forest environment: +3 Speed for Rangers!")
            elif environment == "Space Base":
                enemy.attack += 5  # Enemies stronger in their territory
                print("🚀 Space Base: Enemies are more dangerous here!")
            elif environment == "Underwater":
                player.defense += 2  # Ranger suits provide protection
                enemy.speed -= 2  # Enemies slower underwater
                print("🌊 Underwater: +2 Defense for Rangers, -2 Speed for enemies!")
            elif environment == "Mountain":
                player.attack += 3  # High ground advantage
                print("⛰️ Mountain Peak: +3 Attack for Rangers!")
            elif environment == "City":
                player.mega_energy += 1  # Morphin Grid stronger in populated areas
                print("🏙️ City: +1 Mega Energy from civilian support!")
                
        except Exception as e:
            print(f"Error applying environment effects: {e}")
    
    def _battle_loop(self, player, enemy, environment):
        """Main battle loop"""
        try:
            while player.is_alive() and enemy.is_alive():
                self.turn_counter += 1
                print(f"\n--- TURN {self.turn_counter} ---")
                
                # Show status
                self._show_battle_status(player, enemy)
                
                # Player turn
                if player.is_alive():
                    player_action = self._get_player_action(player, enemy)
                    if player_action == "flee":
                        return {"result": "fled", "message": "You fled from battle!"}
                    
                    self._execute_player_action(player, enemy, player_action)
                
                # Check if enemy is defeated
                if not enemy.is_alive():
                    return self._handle_victory(player, enemy)
                
                # Enemy turn
                if enemy.is_alive():
                    self._execute_enemy_turn(player, enemy)
                
                # Check if player is defeated
                if not player.is_alive():
                    return self._handle_defeat(player, enemy)
                
                # Update status effects
                self._update_status_effects(player, enemy)
                
                # Regenerate some mega energy
                if self.turn_counter % 3 == 0:
                    player.mega_energy = min(5, player.mega_energy + 1)
                
                input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            return {"result": "interrupted", "message": "Battle interrupted!"}
        except Exception as e:
            print(f"Error in battle loop: {e}")
            return {"result": "error", "message": "Battle system error"}
    
    def _show_battle_status(self, player, enemy):
        """Show current battle status"""
        try:
            print(f"\n🦸 {player.name}: {player.get_health_bar()}")
            print(f"⚡ Mega Energy: {player.mega_energy}")
            
            if player.limb_damage["arms"] > 0 or player.limb_damage["legs"] > 0:
                print(f"🩹 Injuries: Arms({player.limb_damage['arms']}) Legs({player.limb_damage['legs']})")
            
            print(f"\n👹 {enemy.name}: {enemy.get_health_bar()}")
            print(f"🧠 State: {enemy.state.value}")
            print(f"📊 {enemy.get_status_description()}")
            
        except Exception as e:
            print(f"Error showing battle status: {e}")
    
    def _get_player_action(self, player, enemy):
        """Get player's action choice"""
        try:
            print(f"\n🎮 CHOOSE YOUR ACTION:")
            print("1. 👊 Attack")
            print("2. 🛡️ Defend")
            print("3. ⚡ Use Skill")
            print("4. 🎯 Target Limb")
            print("5. 🔥 Combo Attack")
            print("6. 🌟 Fusion Power" + (" (AVAILABLE!)" if player.can_use_fusion_power() else " (Locked)"))
            print("7. 💊 Use Item")
            print("8. 🏃 Flee")
            
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == "1":
                return "attack"
            elif choice == "2":
                return "defend"
            elif choice == "3":
                return self._choose_skill(player)
            elif choice == "4":
                return self._choose_limb_target(enemy)
            elif choice == "5":
                return "combo"
            elif choice == "6":
                if player.can_use_fusion_power():
                    return "fusion"
                else:
                    print("❌ Fusion Power not available!")
                    return self._get_player_action(player, enemy)
            elif choice == "7":
                return "item"
            elif choice == "8":
                return "flee"
            else:
                print("❌ Invalid choice!")
                return self._get_player_action(player, enemy)
                
        except Exception as e:
            print(f"Error getting player action: {e}")
            return "attack"
    
    def _choose_skill(self, player):
        """Let player choose a skill to use"""
        try:
            available_skills = [skill for skill, learned in player.skills.items() if learned]
            
            if not available_skills:
                print("❌ No skills available!")
                return "attack"
            
            print(f"\n⚡ AVAILABLE SKILLS:")
            for i, skill in enumerate(available_skills, 1):
                print(f"{i}. {skill}")
            print(f"{len(available_skills) + 1}. Cancel")
            
            choice = input(f"\nChoose skill (1-{len(available_skills) + 1}): ").strip()
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(available_skills):
                    return ("skill", available_skills[choice_num - 1])
                elif choice_num == len(available_skills) + 1:
                    return self._get_player_action(player, None)
                else:
                    print("❌ Invalid choice!")
                    return self._choose_skill(player)
            except ValueError:
                print("❌ Please enter a number!")
                return self._choose_skill(player)
                
        except Exception as e:
            print(f"Error choosing skill: {e}")
            return "attack"
    
    def _choose_limb_target(self, enemy):
        """Let player choose which limb to target"""
        try:
            available_limbs = [name for name, limb in enemy.limbs.items() if not limb["broken"]]
            
            if not available_limbs:
                print("❌ No targetable limbs!")
                return "attack"
            
            print(f"\n🎯 TARGET LIMB:")
            for i, limb in enumerate(available_limbs, 1):
                limb_data = enemy.limbs[limb]
                print(f"{i}. {limb.replace('_', ' ').title()} ({limb_data['health']}/{limb_data['max_health']} HP)")
            print(f"{len(available_limbs) + 1}. Cancel")
            
            choice = input(f"\nChoose target (1-{len(available_limbs) + 1}): ").strip()
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(available_limbs):
                    return ("limb_attack", available_limbs[choice_num - 1])
                elif choice_num == len(available_limbs) + 1:
                    return self._get_player_action(player, None)
                else:
                    print("❌ Invalid choice!")
                    return self._choose_limb_target(enemy)
            except ValueError:
                print("❌ Please enter a number!")
                return self._choose_limb_target(enemy)
                
        except Exception as e:
            print(f"Error choosing limb target: {e}")
            return "attack"
    
    def _execute_player_action(self, player, enemy, action):
        """Execute the player's chosen action"""
        try:
            if action == "attack":
                damage = player.attack + random.randint(-3, 5)
                actual_damage = enemy.take_damage(damage)
                message = f"🗡️ {player.name} attacks for {actual_damage} damage!"
                print(message)
                self.battle_log.append(message)
                
            elif action == "defend":
                # Only heal if player has Medic Protocol skill
                if player.skills.get("Medic Protocol", False):
                    heal_amount = player.max_health * 0.1
                    player.heal(heal_amount)
                    message = f"🛡️ {player.name} defends and heals {heal_amount:.0f} health!"
                else:
                    player.defense += 3  # Temporary defense boost
                    message = f"🛡️ {player.name} takes a defensive stance! (+3 Defense)"
                print(message)
                self.battle_log.append(message)
                
            elif isinstance(action, tuple) and action[0] == "skill":
                skill_name = action[1]
                success, skill_message = player.use_skill(skill_name)
                if success:
                    if "damage" in skill_message.lower():
                        # Extract damage and apply to enemy
                        import re
                        damage_match = re.search(r'(\d+)', skill_message)
                        if damage_match:
                            damage = int(damage_match.group(1))
                            actual_damage = enemy.take_damage(damage)
                            message = f"⚡ {skill_name}: {actual_damage} damage dealt!"
                        else:
                            message = f"⚡ {skill_message}"
                    else:
                        message = f"⚡ {skill_message}"
                else:
                    message = f"❌ {skill_message}"
                print(message)
                self.battle_log.append(message)
                
            elif isinstance(action, tuple) and action[0] == "limb_attack":
                limb_name = action[1]
                damage = player.attack + random.randint(-2, 3)
                success, limb_message = enemy.take_limb_damage(limb_name, damage)
                if success:
                    # Also deal some regular damage
                    regular_damage = damage // 2
                    enemy.take_damage(regular_damage)
                    message = f"🎯 Targeted {limb_name}: {limb_message} (+{regular_damage} body damage)"
                else:
                    message = f"🎯 {limb_message}"
                print(message)
                self.battle_log.append(message)
                
            elif action == "combo":
                self._execute_combo_attack(player, enemy)
                
            elif action == "fusion":
                success, fusion_message = player.use_fusion_power()
                if success:
                    # Extract damage and apply to enemy
                    import re
                    damage_match = re.search(r'(\d+)', fusion_message)
                    if damage_match:
                        damage = int(damage_match.group(1))
                        actual_damage = enemy.take_damage(damage)
                        message = f"🌟 FUSION POWER: {actual_damage} MASSIVE damage dealt!"
                    else:
                        message = fusion_message
                else:
                    message = f"❌ {fusion_message}"
                print(message)
                self.battle_log.append(message)
                
            elif action == "item":
                message = "💊 No items available yet!"
                print(message)
                self.battle_log.append(message)
                
        except Exception as e:
            print(f"Error executing player action: {e}")
            message = f"❌ Action failed due to error!"
            self.battle_log.append(message)
    
    def _execute_combo_attack(self, player, enemy):
        """Execute quick-time event combo attack"""
        try:
            print(f"\n🔥 COMBO ATTACK INITIATED!")
            print("Quick! Enter the button sequence:")
            
            # Generate random sequence
            sequence_length = random.randint(3, 8)
            required_sequence = [random.choice(Config.COMBO_KEYS) for _ in range(sequence_length)]
            
            print(f"Sequence: {' → '.join(required_sequence)}")
            print(f"You have {Config.COMBO_TIME_LIMIT} seconds!")
            
            # Get player input with timer
            start_time = time.time()
            player_input = input("Enter sequence (separated by spaces): ").strip().upper().split()
            end_time = time.time()
            
            time_taken = end_time - start_time
            
            if time_taken > Config.COMBO_TIME_LIMIT:
                message = f"⏰ Too slow! Combo failed! ({time_taken:.1f}s)"
                print(message)
                self.battle_log.append(message)
                return
            
            # Check sequence accuracy
            if player_input == required_sequence:
                # Perfect combo
                damage = player.attack * Config.COMBO_DAMAGE_MULTIPLIER
                actual_damage = enemy.take_damage(damage)
                message = f"🎯 PERFECT COMBO! {actual_damage} damage dealt! ({time_taken:.1f}s)"
                
                # Chance for critical effect
                if time_taken < Config.COMBO_TIME_LIMIT * 0.5:  # Very fast
                    if random.random() < 0.3:  # 30% chance
                        enemy.status_effects.append({"type": "stunned", "duration": 1})
                        message += " Enemy stunned!"
                
            elif len(player_input) == len(required_sequence):
                # Partial match
                correct_count = sum(1 for i, key in enumerate(player_input) 
                                  if i < len(required_sequence) and key == required_sequence[i])
                accuracy = correct_count / len(required_sequence)
                
                if accuracy >= 0.6:  # 60% or better
                    damage = player.attack * (1 + accuracy)
                    actual_damage = enemy.take_damage(damage)
                    message = f"✨ Good combo! {actual_damage} damage dealt! ({accuracy*100:.0f}% accuracy)"
                else:
                    damage = player.attack * 0.5
                    actual_damage = enemy.take_damage(damage)
                    message = f"💥 Weak combo. {actual_damage} damage dealt. ({accuracy*100:.0f}% accuracy)"
            else:
                # Wrong length
                damage = player.attack * 0.3
                actual_damage = enemy.take_damage(damage)
                message = f"❌ Combo failed! Only {actual_damage} damage dealt."
            
            print(message)
            self.battle_log.append(message)
            
        except Exception as e:
            print(f"Error executing combo: {e}")
            message = "❌ Combo system error!"
            self.battle_log.append(message)
    
    def _execute_enemy_turn(self, player, enemy):
        """Execute enemy's turn"""
        try:
            action, action_message = enemy.choose_action(player)
            print(f"\n👹 {action_message}")
            
            damage_dealt, result_message = enemy.execute_action(action, player)
            print(f"👹 {result_message}")
            
            self.battle_log.append(f"Enemy: {result_message}")
            
            # Special action results
            if action == "flee" and random.random() < 0.3:
                print(f"💨 {enemy.name} successfully flees from battle!")
                return "enemy_fled"
            
        except Exception as e:
            print(f"Error executing enemy turn: {e}")
            self.battle_log.append("Enemy: Action failed!")
    
    def _update_status_effects(self, player, enemy):
        """Update status effects for both combatants"""
        try:
            # Update player status effects
            player.status_effects = [effect for effect in player.status_effects 
                                   if effect.get("duration", 0) > 0]
            for effect in player.status_effects:
                effect["duration"] -= 1
            
            # Update enemy status effects (already handled in enemy.choose_action)
            
        except Exception as e:
            print(f"Error updating status effects: {e}")
    
    def _handle_victory(self, player, enemy):
        """Handle player victory"""
        try:
            print(f"\n🎉 VICTORY!")
            print("=" * 30)
            
            # Calculate rewards
            base_gold = enemy.gold_reward
            base_xp = enemy.xp_reward
            
            # Bonus for perfect health
            health_bonus = 1.0
            if player.current_health == player.max_health:
                health_bonus = 1.5
                print("💪 Perfect Health Bonus: +50% rewards!")
            elif player.current_health >= player.max_health * 0.8:
                health_bonus = 1.2
                print("💚 Good Health Bonus: +20% rewards!")
            
            # Bonus for combo usage
            combo_bonus = 1.0
            combo_count = sum(1 for log in self.battle_log if "COMBO" in log)
            if combo_count > 0:
                combo_bonus = 1 + (combo_count * 0.1)
                print(f"🔥 Combo Bonus: +{combo_count * 10}% rewards!")
            
            # Calculate final rewards
            final_gold = int(base_gold * health_bonus * combo_bonus)
            final_xp = int(base_xp * health_bonus * combo_bonus)
            
            # Apply rewards
            player.gold += final_gold
            leveled_up = player.gain_xp(final_xp)
            
            print(f"💰 Gold earned: {final_gold}")
            print(f"⭐ XP earned: {final_xp}")
            
            # Chance for Ranger Key
            if random.random() < 0.3:  # 30% chance
                ranger_keys = [
                    "Red Ranger Key", "Blue Ranger Key", "Yellow Ranger Key",
                    "Pink Ranger Key", "Black Ranger Key", "Green Ranger Key",
                    "White Ranger Key", "Gold Ranger Key", "Silver Ranger Key"
                ]
                key = random.choice(ranger_keys)
                if player.add_ranger_key(key):
                    print(f"🔑 Bonus: Found {key}!")
            
            # Add to battle history
            battle_record = {
                "enemy": enemy.name,
                "result": "victory",
                "turns": self.turn_counter,
                "gold_earned": final_gold,
                "xp_earned": final_xp,
                "timestamp": time.time()
            }
            player.battle_history.append(battle_record)
            
            return {
                "result": "victory",
                "gold_earned": final_gold,
                "xp_earned": final_xp,
                "leveled_up": leveled_up,
                "battle_log": self.battle_log
            }
            
        except Exception as e:
            print(f"Error handling victory: {e}")
            return {"result": "victory", "gold_earned": 0, "xp_earned": 0}
    
    def _handle_defeat(self, player, enemy):
        """Handle player defeat"""
        try:
            print(f"\n💀 DEFEAT!")
            print("=" * 20)
            print(f"You were defeated by {enemy.name}!")
            
            # Penalty for defeat
            gold_lost = min(player.gold * 0.1, 50)  # Lose 10% gold, max 50
            player.gold -= gold_lost
            player.gold = max(0, player.gold)
            
            # Restore some health
            player.current_health = player.max_health * 0.3
            
            print(f"💸 Lost {gold_lost:.0f} gold")
            print(f"❤️ Restored to {player.current_health:.0f} health")
            
            # Add to battle history
            battle_record = {
                "enemy": enemy.name,
                "result": "defeat",
                "turns": self.turn_counter,
                "gold_lost": gold_lost,
                "timestamp": time.time()
            }
            player.battle_history.append(battle_record)
            
            return {
                "result": "defeat",
                "gold_lost": gold_lost,
                "battle_log": self.battle_log
            }
            
        except Exception as e:
            print(f"Error handling defeat: {e}")
            return {"result": "defeat", "gold_lost": 0}
