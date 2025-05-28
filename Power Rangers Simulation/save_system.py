import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import glob
import shutil

class SaveSystem:
    def __init__(self, save_directory: str = "saves"):
        self.save_directory = save_directory
        self.max_save_slots = 5
        self.backup_directory = os.path.join(save_directory, "backups")
        self.ensure_save_directory()
    
    def ensure_save_directory(self):
        """Create save directory and backup directory if they don't exist"""
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
        if not os.path.exists(self.backup_directory):
            os.makedirs(self.backup_directory)
    
    def get_save_files(self) -> List[Dict]:
        """Get list of all save files with metadata"""
        save_files = []
        pattern = os.path.join(self.save_directory, "save*.json")
        
        for filepath in glob.glob(pattern):
            # Skip backup directory files
            if self.backup_directory in filepath:
                continue
                
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                # Extract save metadata
                save_info = {
                    "filename": os.path.basename(filepath),
                    "slot": int(os.path.basename(filepath).replace("save", "").replace(".json", "")),
                    "character_name": data.get("character", {}).get("name", "Unknown"),
                    "level": data.get("character", {}).get("level", 1),
                    "timestamp": data.get("save_timestamp", "Unknown"),
                    "battles_won": len([b for b in data.get("character", {}).get("battle_history", []) if b.get("result") == "victory"]),
                    "gold": data.get("character", {}).get("gold", 0)
                }
                save_files.append(save_info)
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                # Log corrupted save files
                print(f"Warning: Corrupted save file {filepath}: {e}")
                continue
        
        return sorted(save_files, key=lambda x: x["slot"])
    
    def save_game(self, slot: int, character, stock_market, game_state: Dict = None) -> bool:
        """Save game to specified slot with backup"""
        try:
            # Create backup of existing save if it exists
            self.backup_save(slot)
            
            save_data = {
                "save_timestamp": datetime.now().isoformat(),
                "game_version": "2.0",
                "character": character.get_stats_dict(),
                "stock_market": {
                    "commodities": stock_market.commodities,
                    "price_history": stock_market.price_history,
                    "market_events": stock_market.market_events
                },
                "game_state": game_state or {}
            }
            
            filename = f"save{slot}.json"
            filepath = os.path.join(self.save_directory, filename)
            
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            print(f"✅ Game saved to slot {slot}!")
            return True
            
        except Exception as e:
            print(f"❌ Error saving game: {e}")
            return False
    
    def load_game(self, slot: int) -> Optional[Dict]:
        """Load game from specified slot with validation and error recovery"""
        try:
            filename = f"save{slot}.json"
            filepath = os.path.join(self.save_directory, filename)
            
            if not os.path.exists(filepath):
                print(f"❌ Save file {filename} not found!")
                return None
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Validate save file structure
            if not self.validate_save_data(data):
                print(f"❌ Save file {filename} is corrupted!")
                
                # Try to load backup
                backup_path = self._get_latest_backup(slot)
                if backup_path:
                    print(f"🔄 Attempting to load backup...")
                    with open(backup_path, 'r') as f:
                        backup_data = json.load(f)
                    
                    if self.validate_save_data(backup_data):
                        print(f"✅ Backup loaded successfully!")
                        return backup_data
                    else:
                        print(f"❌ Backup is also corrupted!")
                
                return None
            
            print(f"✅ Game loaded from slot {slot}!")
            return data
            
        except json.JSONDecodeError:
            print(f"❌ Save file {filename} is corrupted (JSON error)!")
            # Try to load backup
            backup_path = self._get_latest_backup(slot)
            if backup_path:
                try:
                    print(f"🔄 Attempting to load backup...")
                    with open(backup_path, 'r') as f:
                        backup_data = json.load(f)
                    
                    if self.validate_save_data(backup_data):
                        print(f"✅ Backup loaded successfully!")
                        return backup_data
                except:
                    print(f"❌ Backup is also corrupted!")
            
            return None
        except Exception as e:
            print(f"❌ Error loading game: {e}")
            return None
    
    def validate_save_data(self, data: Dict) -> bool:
        """Validate save file structure with detailed checks"""
        try:
            required_keys = ["character", "stock_market", "save_timestamp"]
            
            # Check top-level structure
            for key in required_keys:
                if key not in data:
                    print(f"Missing required key: {key}")
                    return False
            
            # Check character data
            character_data = data["character"]
            required_character_keys = ["name", "color", "power_type", "weapon", "level", 
                                      "max_health", "current_health", "attack", "defense", 
                                      "speed", "gold", "mega_energy"]
            
            for key in required_character_keys:
                if key not in character_data:
                    print(f"Missing character data: {key}")
                    return False
            
            # Check stock market data
            market_data = data["stock_market"]
            if "commodities" not in market_data:
                print("Missing stock market commodities")
                return False
            
            # Validate data types
            if not isinstance(character_data["level"], int):
                print("Invalid level data type")
                return False
                
            if not isinstance(character_data["gold"], (int, float)):
                print("Invalid gold data type")
                return False
            
            return True
        except Exception as e:
            print(f"Error validating save data: {e}")
            return False
    
    def show_save_menu(self) -> int:
        """Display save menu and get user choice"""
        save_files = self.get_save_files()
        
        print("\n💾 SAVE GAME 💾")
        print("=" * 30)
        
        # Show existing saves
        for i in range(1, self.max_save_slots + 1):  # Show slots 1-5
            existing_save = next((s for s in save_files if s["slot"] == i), None)
            
            if existing_save:
                timestamp = existing_save["timestamp"]
                if timestamp != "Unknown":
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        timestamp = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        pass
                
                print(f"{i}. {existing_save['character_name']} (Lv.{existing_save['level']}) - {timestamp}")
                print(f"   💰 {existing_save['gold']} gold, 🏆 {existing_save['battles_won']} victories")
            else:
                print(f"{i}. [Empty Slot]")
        
        print(f"{self.max_save_slots + 1}. Cancel")
        
        while True:
            try:
                choice = int(input(f"\nSelect save slot (1-{self.max_save_slots + 1}): "))
                if 1 <= choice <= self.max_save_slots + 1:
                    return choice
                else:
                    print(f"Invalid choice! Please select 1-{self.max_save_slots + 1}.")
            except ValueError:
                print("Please enter a number!")
    
    def show_load_menu(self) -> int:
        """Display load menu and get user choice"""
        save_files = self.get_save_files()
        
        if not save_files:
            print("\n❌ No save files found!")
            return 0
        
        print("\n📁 LOAD GAME 📁")
        print("=" * 30)
        
        # Show existing saves
        for save_file in save_files:
            timestamp = save_file["timestamp"]
            if timestamp != "Unknown":
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    timestamp = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
            
            print(f"{save_file['slot']}. {save_file['character_name']} (Lv.{save_file['level']}) - {timestamp}")
            print(f"   💰 {save_file['gold']} gold, 🏆 {save_file['battles_won']} victories")
        
        print("0. Cancel")
        
        valid_slots = [s["slot"] for s in save_files] + [0]
        
        while True:
            try:
                choice = int(input(f"\nSelect save slot ({'/'.join(map(str, valid_slots))}): "))
                if choice in valid_slots:
                    return choice
                else:
                    print(f"Invalid choice! Please select from: {'/'.join(map(str, valid_slots))}")
            except ValueError:
                print("Please enter a number!")
    
    def backup_save(self, slot: int) -> bool:
        """Create backup of save file"""
        try:
            filename = f"save{slot}.json"
            filepath = os.path.join(self.save_directory, filename)
            
            if not os.path.exists(filepath):
                return False  # No file to backup
                
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"save{slot}_backup_{timestamp}.json"
            backup_filepath = os.path.join(self.backup_directory, backup_filename)
            
            # Copy the file to backup
            shutil.copy2(filepath, backup_filepath)
            
            # Clean up old backups (keep only 3 most recent per slot)
            self._cleanup_old_backups(slot)
            
            return True
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return False
    
    def _cleanup_old_backups(self, slot: int):
        """Keep only the 3 most recent backups per slot"""
        try:
            pattern = os.path.join(self.backup_directory, f"save{slot}_backup_*.json")
            backups = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
            
            # Keep only the 3 most recent backups
            for old_backup in backups[3:]:
                os.remove(old_backup)
        except Exception as e:
            print(f"Warning: Error cleaning up old backups: {e}")
    
    def _get_latest_backup(self, slot: int) -> Optional[str]:
        """Get the path to the latest backup for a slot"""
        try:
            pattern = os.path.join(self.backup_directory, f"save{slot}_backup_*.json")
            backups = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
            
            if backups:
                return backups[0]
            return None
        except Exception as e:
            print(f"Error finding backup: {e}")
            return None
