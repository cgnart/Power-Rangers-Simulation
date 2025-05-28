import random
import time
from character import PowerRanger
from enemy import create_enemy
from stock_market import StockMarket
from save_system import SaveSystem
from battle import BattleSystem
from mission import MissionSystem
from config import Config
from exceptions import InvalidMove, InsufficientFunds, MarketException, SaveError, LoadError, SkillError
from utils import calculate_damage, apply_status_effect, is_critical_hit
import itertools
import collections

class PowerRangersGame:
    def __init__(self):
        self.ranger = None
        self.stock_market = StockMarket()
        self.save_system = SaveSystem()
        self.battle_system = BattleSystem()
        self.mission_system = MissionSystem()
        self.game_running = True
        
        print("🌟 Power Rangers Megaforce Enhanced Edition v2.0")
        print("Bug-Fixed and Feature-Complete Version")
        print("=" * 50)
    
    def show_main_menu(self):
        """Display main menu and get user choice"""
        try:
            print(f"\n🎮 POWER RANGERS MEGAFORCE - MAIN MENU")
            print("=" * 45)
            
            if self.ranger:
                print(f"👤 Current Ranger: {self.ranger.name} ({self.ranger.color})")
                print(f"💰 Gold: {self.ranger.gold:.2f}")
                print(f"📊 Level: {self.ranger.level}")
                print()
            
            print("1. 🆕 New Game")
            print("2. 📁 Load Game")
            print("3. 💾 Save Game")
            print("4. ⚔️ Quick Battle")
            print("5. 🎯 Missions")
            print("6. 📊 Stock Market")
            print("7. 👤 Character Info")
            print("8. 🎯 Skills Menu")
            print("9. 📈 Statistics")
            print("10. ⚙️ Settings")
            print("11. 🚪 Exit Game")
            
            choice = input(f"\nEnter your choice (1-11): ").strip()
            
            try:
                return int(choice)
            except ValueError:
                print("❌ Please enter a number!")
                return self.show_main_menu()
                
        except Exception as e:
            print(f"Error showing main menu: {e}")
            return 11  # Exit on error
    
    def new_game(self):
        """Start a new game with character creation"""
        try:
            print(f"\n🆕 NEW GAME - CHARACTER CREATION")
            print("=" * 40)
            
            # Get character name
            name = input("Enter your Ranger name: ").strip()
            if not name:
                name = "Ranger"
            
            # Choose color
            colors = list(Config.COLOR_BONUSES.keys())
            print(f"\n🎨 Choose your Ranger color:")
            for i, color in enumerate(colors, 1):
                bonus = Config.COLOR_BONUSES[color]
                print(f"{i}. {color} (+{bonus['health']} Health, +{bonus.get('attack', 0)} Attack)")
            
            color_choice = self._get_choice_input(len(colors), "color")
            chosen_color = colors[color_choice - 1]
            
            # Choose power type
            power_types = list(Config.POWER_BONUSES.keys())
            print(f"\n⚡ Choose your Power Type:")
            for i, power in enumerate(power_types, 1):
                bonus = Config.POWER_BONUSES[power]
                print(f"{i}. {power} (+{bonus.get('attack', 0)} Attack, Special: {bonus['special']})")
            
            power_choice = self._get_choice_input(len(power_types), "power type")
            chosen_power = power_types[power_choice - 1]
            
            # Choose weapon
            weapons = list(Config.WEAPON_STATS.keys())
            print(f"\n⚔️ Choose your weapon:")
            for i, weapon in enumerate(weapons, 1):
                stats = Config.WEAPON_STATS[weapon]
                speed_text = f"+{stats['speed']}" if stats['speed'] >= 0 else str(stats['speed'])
                print(f"{i}. {weapon} (+{stats['damage']} Damage, {speed_text} Speed)")
            
            weapon_choice = self._get_choice_input(len(weapons), "weapon")
            chosen_weapon = weapons[weapon_choice - 1]
            
            # Create character
            self.ranger = PowerRanger(name, chosen_color, chosen_power, chosen_weapon)
            
            # Show final stats
            print(f"\n✅ CHARACTER CREATED!")
            print("=" * 25)
            print(f"🦸 Name: {self.ranger.name}")
            print(f"🎨 Color: {self.ranger.color}")
            print(f"⚡ Power: {self.ranger.power_type}")
            print(f"⚔️ Weapon: {self.ranger.weapon}")
            print(f"\n📊 FINAL STATS:")
            print(f"❤️ Health: {self.ranger.max_health}")
            print(f"⚔️ Attack: {self.ranger.attack}")
            print(f"🛡️ Defense: {self.ranger.defense}")
            print(f"💨 Speed: {self.ranger.speed}")
            print(f"💰 Starting Gold: {self.ranger.gold}")
            
            input("\nPress Enter to begin your adventure...")
            
        except Exception as e:
            print(f"Error creating new game: {e}")
    
    def _get_choice_input(self, max_choice, choice_type):
        """Get valid choice input from user"""
        try:
            choice = input(f"\nChoose your {choice_type} (1-{max_choice}): ").strip()
            choice_num = int(choice)
            
            if 1 <= choice_num <= max_choice:
                return choice_num
            else:
                print(f"❌ Please choose a number between 1 and {max_choice}!")
                return self._get_choice_input(max_choice, choice_type)
                
        except ValueError:
            print("❌ Please enter a number!")
            return self._get_choice_input(max_choice, choice_type)
    
    def load_game(self):
        """Load a saved game"""
        try:
            if not self.ranger:
                print("ℹ️ Loading saved game...")
            
            slot = self.save_system.show_load_menu()
            
            if slot == 0:  # Cancel
                return
            
            save_data = self.save_system.load_game(slot)
            
            if save_data:
                # Create new character and load data
                self.ranger = PowerRanger()
                success = self.ranger.load_from_dict(save_data["character"])
                
                if success:
                    # Load stock market data
                    self.stock_market.load_market_data(save_data["stock_market"])
                    
                    print(f"✅ Game loaded successfully!")
                    print(f"👤 Welcome back, {self.ranger.name}!")
                    print(f"📊 Level {self.ranger.level} {self.ranger.color} Ranger")
                    print(f"💰 Gold: {self.ranger.gold}")
                else:
                    print("❌ Error loading character data!")
                    self.ranger = None
            else:
                print("❌ Failed to load game!")
                
        except Exception as e:
            print(f"Error loading game: {e}")
    
    def save_game(self):
        """Save the current game"""
        try:
            if not self.ranger:
                print("❌ No game to save! Start a new game first.")
                return
            
            slot = self.save_system.show_save_menu()
            
            if slot > self.save_system.max_save_slots:  # Cancel
                return
            
            # Update stock market before saving
            self.stock_market.update_prices()
            
            success = self.save_system.save_game(slot, self.ranger, self.stock_market)
            
            if success:
                print(f"✅ Game saved to slot {slot}!")
            else:
                print("❌ Failed to save game!")
                
        except Exception as e:
            print(f"Error saving game: {e}")
    
    def quick_battle(self):
        """Start a quick battle"""
        try:
            if not self.ranger:
                print("❌ Create a character first!")
                return
            
            print(f"\n⚔️ QUICK BATTLE")
            print("=" * 20)
            
            # Choose difficulty
            difficulties = ["Easy", "Medium", "Hard", "Extreme"]
            print("Choose difficulty:")
            for i, diff in enumerate(difficulties, 1):
                print(f"{i}. {diff}")
            
            diff_choice = self._get_choice_input(len(difficulties), "difficulty")
            chosen_difficulty = difficulties[diff_choice - 1]
            
            # Create random enemy
            enemy = create_enemy("random", chosen_difficulty)
            
            # Choose environment
            environments = ["City", "Forest", "Space Base", "Underwater", "Mountain"]
            print("\nChoose battle environment:")
            for i, env in enumerate(environments, 1):
                print(f"{i}. {env}")
            
            env_choice = self._get_choice_input(len(environments), "environment")
            chosen_environment = environments[env_choice - 1]
            
            # Start battle
            battle_result = self.battle_system.start_battle(self.ranger, enemy, chosen_environment)
            
            # Update stock market based on battle outcome
            if battle_result["result"] == "victory":
                self.stock_market.update_prices("victory")
            elif battle_result["result"] == "defeat":
                self.stock_market.update_prices("defeat")
            
            input("\nPress Enter to continue...")
            
        except Exception as e:
            print(f"Error in quick battle: {e}")
    
    def missions_menu(self):
        """Show missions menu"""
        try:
            if not self.ranger:
                print("❌ Create a character first!")
                return
            
            while True:
                print(f"\n🎯 MISSIONS MENU")
                print("=" * 20)
                print("1. 📋 Available Missions")
                print("2. 📜 Mission History")
                print("3. 🔄 Refresh Missions")
                print("4. 🔙 Back to Main Menu")
                
                choice = input("\nEnter your choice (1-4): ").strip()
                
                if choice == "1":
                    result = self.mission_system.select_mission(self.ranger)
                    if result:
                        # Update stock market after mission
                        if result["success"]:
                            self.stock_market.update_prices("victory")
                        else:
                            self.stock_market.update_prices("defeat")
                        input("\nPress Enter to continue...")
                elif choice == "2":
                    self.mission_system.show_mission_history(self.ranger)
                    input("\nPress Enter to continue...")
                elif choice == "3":
                    self.mission_system.generate_missions()
                    print("✅ New missions generated!")
                elif choice == "4":
                    break
                else:
                    print("❌ Invalid choice!")
                    
        except Exception as e:
            print(f"Error in missions menu: {e}")
    
    def stock_market_menu(self):
        """Show stock market menu"""
        try:
            if not self.ranger:
                print("❌ Create a character first!")
                return
            
            while True:
                # Update prices
                self.stock_market.update_prices()
                
                print(f"\n📊 STOCK MARKET")
                print("=" * 25)
                print(f"💰 Your Gold: {self.ranger.gold:.2f}")
                portfolio_value = self.stock_market.get_portfolio_value(self.ranger)
                print(f"💼 Portfolio Value: {portfolio_value:.2f}")
                print()
                
                print("1. 📈 Market Status")
                print("2. 💼 Your Portfolio")
                print("3. 💰 Buy Commodities")
                print("4. 💸 Sell Commodities")
                print("5. 📰 Market News")
                print("6. 🔙 Back to Main Menu")
                
                choice = input("\nEnter your choice (1-6): ").strip()
                
                if choice == "1":
                    self.stock_market.show_market_status()
                    input("\nPress Enter to continue...")
                elif choice == "2":
                    self.stock_market.show_portfolio(self.ranger)
                    input("\nPress Enter to continue...")
                elif choice == "3":
                    self._buy_commodities()
                elif choice == "4":
                    self._sell_commodities()
                elif choice == "5":
                    self._show_market_news()
                    input("\nPress Enter to continue...")
                elif choice == "6":
                    break
                else:
                    print("❌ Invalid choice!")
                    
        except Exception as e:
            print(f"Error in stock market menu: {e}")
    
    def _buy_commodities(self):
        """Handle commodity buying"""
        try:
            commodities = list(self.stock_market.commodities.keys())
            
            print(f"\n💰 BUY COMMODITIES")
            print("=" * 25)
            print(f"Your Gold: {self.ranger.gold:.2f}")
            print()
            
            for i, name in enumerate(commodities, 1):
                price = self.stock_market.commodities[name]["price"]
                print(f"{i}. {name} - {price:.2f} gold each")
            print(f"{len(commodities) + 1}. Cancel")
            
            choice = input(f"\nChoose commodity (1-{len(commodities) + 1}): ").strip()
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(commodities):
                    commodity_name = commodities[choice_num - 1]
                    price = self.stock_market.commodities[commodity_name]["price"]
                    
                    max_affordable = int(self.ranger.gold // price)
                    if max_affordable == 0:
                        print(f"❌ You can't afford any {commodity_name}!")
                        return
                    
                    print(f"You can afford up to {max_affordable} units")
                    amount_str = input(f"How many {commodity_name} to buy? ").strip()
                    
                    amount = int(amount_str)
                    if amount <= 0:
                        print("❌ Invalid amount!")
                        return
                    
                    success, message = self.stock_market.buy_commodity(self.ranger, commodity_name, amount)
                    print(f"{'✅' if success else '❌'} {message}")
                    
                elif choice_num == len(commodities) + 1:
                    return
                else:
                    print("❌ Invalid choice!")
                    
            except ValueError:
                print("❌ Please enter a number!")
                
        except Exception as e:
            print(f"Error buying commodities: {e}")
    
    def _sell_commodities(self):
        """Handle commodity selling"""
        try:
            if not self.ranger.investments:
                print("❌ You don't own any commodities!")
                return
            
            owned_commodities = list(self.ranger.investments.keys())
            
            print(f"\n💸 SELL COMMODITIES")
            print("=" * 25)
            
            for i, name in enumerate(owned_commodities, 1):
                amount = self.ranger.investments[name]["amount"]
                current_price = self.stock_market.commodities[name]["price"]
                value = amount * current_price
                print(f"{i}. {name} - {amount:.1f} units (Value: {value:.2f} gold)")
            print(f"{len(owned_commodities) + 1}. Cancel")
            
            choice = input(f"\nChoose commodity (1-{len(owned_commodities) + 1}): ").strip()
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(owned_commodities):
                    commodity_name = owned_commodities[choice_num - 1]
                    owned_amount = self.ranger.investments[commodity_name]["amount"]
                    
                    print(f"You own {owned_amount:.1f} units")
                    amount_str = input(f"How many {commodity_name} to sell? ").strip()
                    
                    amount = float(amount_str)
                    if amount <= 0 or amount > owned_amount:
                        print("❌ Invalid amount!")
                        return
                    
                    success, message = self.stock_market.sell_commodity(self.ranger, commodity_name, amount)
                    print(f"{'✅' if success else '❌'} {message}")
                    
                elif choice_num == len(owned_commodities) + 1:
                    return
                else:
                    print("❌ Invalid choice!")
                    
            except ValueError:
                print("❌ Please enter a number!")
                
        except Exception as e:
            print(f"Error selling commodities: {e}")
    
    def _show_market_news(self):
        """Show market news and events"""
        try:
            print(f"\n📰 MARKET NEWS")
            print("=" * 20)
            
            if not self.stock_market.market_events:
                print("📭 No recent market events")
                return
            
            for event_data in self.stock_market.market_events:
                print(f"• {event_data['event']}")
            
        except Exception as e:
            print(f"Error showing market news: {e}")
    
    def show_character_info(self):
        """Show detailed character information"""
        try:
            if not self.ranger:
                print("❌ Create a character first!")
                return
            
            self.ranger.show_character_sheet()
            input("\nPress Enter to continue...")
            
        except Exception as e:
            print(f"Error showing character info: {e}")
    
    def skills_menu(self):
        """Show skills menu"""
        try:
            if not self.ranger:
                print("❌ Create a character first!")
                return
            
            while True:
                print(f"\n🎯 SKILLS MENU")
                print("=" * 20)
                print(f"⭐ Skill Points: {self.ranger.skill_points}")
                print()
                
                # Show all skills
                available_to_learn = []
                for skill, learned in self.ranger.skills.items():
                    status = "✅ Learned" if learned else "❌ Not learned"
                    print(f"{skill}: {status}")
                    if not learned:
                        available_to_learn.append(skill)
                
                if not available_to_learn:
                    print("\n🎉 All skills learned!")
                    input("Press Enter to continue...")
                    break
                
                if self.ranger.skill_points == 0:
                    print("\n❌ No skill points available!")
                    input("Press Enter to continue...")
                    break
                
                print(f"\n📚 LEARN SKILLS:")
                for i, skill in enumerate(available_to_learn, 1):
                    print(f"{i}. {skill}")
                print(f"{len(available_to_learn) + 1}. Back to main menu")
                
                choice = input(f"\nChoose skill to learn (1-{len(available_to_learn) + 1}): ").strip()
                
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(available_to_learn):
                        skill_name = available_to_learn[choice_num - 1]
                        success, message = self.ranger.learn_skill(skill_name)
                        print(f"{'✅' if success else '❌'} {message}")
                        input("Press Enter to continue...")
                    elif choice_num == len(available_to_learn) + 1:
                        break
                    else:
                        print("❌ Invalid choice!")
                except ValueError:
                    print("❌ Please enter a number!")
                    
        except Exception as e:
            print(f"Error in skills menu: {e}")
    
    def show_statistics(self):
        """Show game statistics"""
        try:
            if not self.ranger:
                print("❌ Create a character first!")
                return
            
            print(f"\n📈 GAME STATISTICS")
            print("=" * 30)
            
            # Character stats
            print(f"👤 CHARACTER:")
            print(f"   Name: {self.ranger.name}")
            print(f"   Level: {self.ranger.level}")
            print(f"   XP: {self.ranger.xp}")
            print(f"   Gold: {self.ranger.gold:.2f}")
            print(f"   Mega Energy: {self.ranger.mega_energy}")
            
            # Battle history
            if self.ranger.battle_history:
                victories = sum(1 for battle in self.ranger.battle_history if battle["result"] == "victory")
                defeats = sum(1 for battle in self.ranger.battle_history if battle["result"] == "defeat")
                total_battles = len(self.ranger.battle_history)
                win_rate = (victories / total_battles * 100) if total_battles > 0 else 0
                
                print(f"\n⚔️ BATTLE RECORD:")
                print(f"   Total Battles: {total_battles}")
                print(f"   Victories: {victories}")
                print(f"   Defeats: {defeats}")
                print(f"   Win Rate: {win_rate:.1f}%")
                
                total_gold_earned = sum(battle.get("gold_earned", 0) for battle in self.ranger.battle_history)
                total_xp_earned = sum(battle.get("xp_earned", 0) for battle in self.ranger.battle_history)
                
                print(f"   Total Gold Earned: {total_gold_earned}")
                print(f"   Total XP Earned: {total_xp_earned}")
            
            # Collection stats
            print(f"\n🔑 COLLECTIONS:")
            print(f"   Ranger Keys: {len(self.ranger.ranger_keys)}")
            print(f"   Skills Learned: {sum(1 for learned in self.ranger.skills.values() if learned)}/{len(self.ranger.skills)}")
            
            # Investment stats
            if self.ranger.investments:
                portfolio_value = self.stock_market.get_portfolio_value(self.ranger)
                profit_loss, profit_loss_percent = self.stock_market.get_portfolio_profit_loss(self.ranger)
                
                print(f"\n💼 INVESTMENTS:")
                print(f"   Portfolio Value: {portfolio_value:.2f} gold")
                print(f"   Profit/Loss: {profit_loss:+.2f} gold ({profit_loss_percent:+.1f}%)")
                print(f"   Commodities Owned: {len(self.ranger.investments)}")
            
            # Mission stats
            completed_missions = len(self.mission_system.completed_missions)
            if completed_missions > 0:
                print(f"\n🎯 MISSIONS:")
                print(f"   Completed: {completed_missions}")
                
                # Mission difficulty breakdown
                easy_missions = sum(1 for m in self.mission_system.completed_missions if m.difficulty == "Easy")
                medium_missions = sum(1 for m in self.mission_system.completed_missions if m.difficulty == "Medium")
                hard_missions = sum(1 for m in self.mission_system.completed_missions if m.difficulty == "Hard")
                extreme_missions = sum(1 for m in self.mission_system.completed_missions if m.difficulty == "Extreme")
                
                print(f"   Easy: {easy_missions}, Medium: {medium_missions}")
                print(f"   Hard: {hard_missions}, Extreme: {extreme_missions}")
            
            input("\nPress Enter to continue...")
            
        except Exception as e:
            print(f"Error showing statistics: {e}")
    
    def settings_menu(self):
        """Show settings menu"""
        try:
            while True:
                print(f"\n⚙️ SETTINGS")
                print("=" * 15)
                print("1. 🔧 Show Bug Fixes")
                print("2. 📖 About Game")
                print("3. 🔙 Back to Main Menu")
                
                choice = input("\nEnter your choice (1-3): ").strip()
                
                if choice == "1":
                    self.show_bug_fixes()
                elif choice == "2":
                    self.show_about()
                elif choice == "3":
                    break
                else:
                    print("❌ Invalid choice!")
                    
        except Exception as e:
            print(f"Error in settings menu: {e}")
    
    def show_bug_fixes(self):
        """Show bug fixes and changes"""
        print("\n🔧 BUG FIXES & ENHANCEMENTS v2.0")
        print("=" * 40)
        
        print("✅ CRITICAL BUG FIXES:")
        print("• Fixed EnemyState error - properly imported and defined")
        print("• Fixed Defend mechanic - only heals with Medic Protocol skill")
        print("• Fixed Combo input - removed SPACE key, uses W/A/S/D/Q/E")
        print("• Added comprehensive error handling throughout")
        print("• Fixed save/load system with validation")
        
        print("\n🆕 NEW FEATURES:")
        print("• Advanced Missions with escalating difficulty")
        print("• Timed survival and VIP escort missions")
        print("• Boss battles with Metal Alice, Black Knight, Emperor Mavro")
        print("• Legendary Ranger Key collection system")
        print("• Fusion Power system requiring level 3+ and Mega Energy")
        print("• Skills system with 5 different skill types")
        print("• Enhanced enemy AI with behavioral states")
        print("• Limb damage system affecting enemy abilities")
        print("• Multi-phase boss battles with armor systems")
        
        print("\n⚖️ BALANCE IMPROVEMENTS:")
        print("• Character creation affects stats based on choices")
        print("• Weapon speed penalties/bonuses properly implemented")
        print("• Mega Energy system limits powerful attacks")
        print("• Skill point economy for character progression")
        print("• Environmental effects in different battle locations")
        
        print("\n🎨 UI/UX IMPROVEMENTS:")
        print("• Wallet visibility in battle and shop menus")
        print("• Battle log tracking for combat history")
        print("• Combo countdown and visual feedback")
        print("• Health bars and progress indicators")
        print("• Colored text and ASCII art throughout")
        print("• Comprehensive statistics tracking")
        
        print("\n🛡️ TECHNICAL IMPROVEMENTS:")
        print("• Try-except blocks prevent crashes")
        print("• Input validation for all user inputs")
        print("• Save file integrity checking")
        print("• Backup save system")
        print("• Modular code architecture")
        print("• Configuration-based balance tweaking")
        
        input("\nPress Enter to continue...")

    def show_about(self):
        """Show about information"""
        print("\n📖 ABOUT")
        print("=" * 15)
        print("🌟 POWER RANGERS MEGAFORCE - ENHANCED EDITION v2.0")
        print("Bug-Fixed and Feature-Complete Version")
        print("\n✨ FEATURES:")
        print("• Dynamic character creation with stat bonuses")
        print("• Real-time stock market system")
        print("• Advanced battle system with limb damage")
        print("• Quick-time event combo system (fixed)")
        print("• Multiple environments and missions")
        print("• Comprehensive save/load system")
        print("• Enemy AI with behavioral states")
        print("• XP progression and skill system")
        print("• Legendary Ranger Key collection")
        print("• Fusion Power and Mega Energy systems")
        print("• Boss battles with multiple phases")
        print("• Mission variety (survival, escort, boss)")
        
        print("\n🎮 BASED ON:")
        print("Power Rangers Megaforce TV Series")
        print("Featuring classic Rangers and villains")
        
        print("\n🔧 TECHNICAL:")
        print("Built with Python 3.8+")
        print("Object-oriented design")
        print("Modular architecture")
        print("Comprehensive error handling")
        print("Save file validation")
        print("Configuration-based balance")
        
        print("\n🐛 BUG FIXES:")
        print("• EnemyState properly defined")
        print("• Defend skill fixed (conditional healing)")
        print("• QTE system uses proper keys (no SPACE)")
        print("• All crashes prevented with try-except")
        print("• Save system validates data integrity")
        
        input("\nPress Enter to continue...")

    def run(self):
        """Main game loop with comprehensive error handling"""
        print("🚀 Starting Power Rangers Megaforce Enhanced v2.0...")
        
        while self.game_running:
            try:
                choice = self.show_main_menu()
                
                if choice == 1:
                    self.new_game()
                elif choice == 2:
                    self.load_game()
                elif choice == 3:
                    self.save_game()
                elif choice == 4:
                    self.quick_battle()
                elif choice == 5:
                    self.missions_menu()
                elif choice == 6:
                    self.stock_market_menu()
                elif choice == 7:
                    self.show_character_info()
                elif choice == 8:
                    self.skills_menu()
                elif choice == 9:
                    self.show_statistics()
                elif choice == 10:
                    self.settings_menu()
                elif choice == 11:
                    self.game_running = False
                    
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Saving progress...")
                if self.ranger:
                    try:
                        # Emergency save
                        self.save_system.save_game(99, self.ranger, self.stock_market)
                        print("Emergency save completed.")
                    except:
                        print("Emergency save failed.")
                print("Thanks for playing Power Rangers Megaforce!")
                break
            except Exception as e:
                print(f"\n❌ An unexpected error occurred: {e}")
                print("Error details:")
                import traceback
                traceback.print_exc()
                print("\nThe game will continue, but consider saving your progress.")
                input("Press Enter to continue...")
        
        print("\n🎉 Thanks for playing Power Rangers Megaforce Enhanced!")
        print("Go Go Megaforce! 🔴🔵🟡🩷⚫🟢")

def main():
    """Entry point for the game with error handling"""
    try:
        print("🌟 Power Rangers Megaforce Enhanced Edition v2.0")
        print("Bug-Fixed and Feature-Complete Version")
        print("=" * 50)
        
        game = PowerRangersGame()
        game.run()
        
    except Exception as e:
        print(f"Fatal error: {e}")
        print("Error details:")
        import traceback
        traceback.print_exc()
        print("\nPlease restart the game.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
