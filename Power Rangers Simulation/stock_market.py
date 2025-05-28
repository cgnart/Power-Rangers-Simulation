import random
import time
from config import Config

class StockMarket:
    def __init__(self):
        self.commodities = {}
        self.price_history = {}
        self.market_events = []
        self.last_update = time.time()
        
        # Initialize commodities
        for name, data in Config.INITIAL_COMMODITIES.items():
            self.commodities[name] = {
                "price": data["price"],
                "volatility": data["volatility"],
                "trend": 0.0,  # -1 to 1, negative is bearish, positive is bullish
                "volume": random.randint(100, 1000)
            }
            self.price_history[name] = [data["price"]]
    
    def update_prices(self, battle_outcome=None):
        """Update commodity prices based on market forces and battle outcomes"""
        try:
            current_time = time.time()
            time_passed = current_time - self.last_update
            
            # Only update if enough time has passed (prevent spam updates)
            if time_passed < 1:
                return
            
            self.last_update = current_time
            
            for name, commodity in self.commodities.items():
                old_price = commodity["price"]
                
                # Base price change from volatility
                volatility = commodity["volatility"]
                trend = commodity["trend"]
                
                # Random market movement
                random_change = random.uniform(-volatility, volatility)
                
                # Trend influence
                trend_change = trend * 0.1
                
                # Battle outcome influence
                battle_change = 0
                if battle_outcome:
                    if battle_outcome == "victory":
                        if name in ["Gold", "Energy Crystals"]:
                            battle_change = 0.05  # Victory increases valuable commodities
                        elif name == "Morphin Grid":
                            battle_change = 0.08  # Big boost for Morphin Grid
                    elif battle_outcome == "defeat":
                        battle_change = -0.03  # Defeat decreases all prices
                
                # Calculate total change
                total_change = random_change + trend_change + battle_change
                
                # Apply change
                new_price = old_price * (1 + total_change)
                
                # Ensure price doesn't go below 10 or above 1000
                new_price = max(10, min(1000, new_price))
                
                commodity["price"] = round(new_price, 2)
                
                # Update price history (keep last 10 prices)
                self.price_history[name].append(new_price)
                if len(self.price_history[name]) > 10:
                    self.price_history[name].pop(0)
                
                # Update trend based on recent price movement
                if len(self.price_history[name]) >= 3:
                    recent_prices = self.price_history[name][-3:]
                    if recent_prices[-1] > recent_prices[0]:
                        commodity["trend"] = min(1.0, commodity["trend"] + 0.1)
                    else:
                        commodity["trend"] = max(-1.0, commodity["trend"] - 0.1)
                
                # Random market events
                if random.random() < 0.05:  # 5% chance per update
                    self._generate_market_event(name)
            
        except Exception as e:
            print(f"Error updating prices: {e}")
    
    def _generate_market_event(self, commodity_name):
        """Generate random market events"""
        try:
            events = [
                f"📈 {commodity_name} demand surges due to Ranger activity!",
                f"📉 {commodity_name} supply increases, prices drop!",
                f"⚡ Energy fluctuations affect {commodity_name} market!",
                f"🌟 New mining operations discovered for {commodity_name}!",
                f"🚨 Monster attacks disrupt {commodity_name} supply chains!"
            ]
            
            event = random.choice(events)
            self.market_events.append({
                "event": event,
                "timestamp": time.time(),
                "commodity": commodity_name
            })
            
            # Keep only last 5 events
            if len(self.market_events) > 5:
                self.market_events.pop(0)
            
            # Apply event effect
            commodity = self.commodities[commodity_name]
            if "surges" in event or "discovered" in event:
                commodity["price"] *= random.uniform(1.1, 1.3)
            elif "drop" in event or "disrupt" in event:
                commodity["price"] *= random.uniform(0.7, 0.9)
            
            commodity["price"] = max(10, min(1000, commodity["price"]))
            
        except Exception as e:
            print(f"Error generating market event: {e}")
    
    def buy_commodity(self, player, commodity_name, amount):
        """Buy commodity with player's gold"""
        try:
            if commodity_name not in self.commodities:
                return False, "Commodity not found!"
            
            commodity = self.commodities[commodity_name]
            total_cost = commodity["price"] * amount
            
            if player.gold < total_cost:
                return False, f"Not enough gold! Need {total_cost:.2f}, have {player.gold:.2f}"
            
            # Execute purchase
            player.gold -= total_cost
            
            if commodity_name not in player.investments:
                player.investments[commodity_name] = {"amount": 0, "avg_price": 0}
            
            # Calculate new average price
            old_amount = player.investments[commodity_name]["amount"]
            old_avg_price = player.investments[commodity_name]["avg_price"]
            
            new_amount = old_amount + amount
            new_avg_price = ((old_amount * old_avg_price) + (amount * commodity["price"])) / new_amount
            
            player.investments[commodity_name]["amount"] = new_amount
            player.investments[commodity_name]["avg_price"] = new_avg_price
            
            return True, f"Bought {amount} {commodity_name} for {total_cost:.2f} gold!"
            
        except Exception as e:
            print(f"Error buying commodity: {e}")
            return False, "Error processing purchase!"
    
    def sell_commodity(self, player, commodity_name, amount):
        """Sell commodity for gold"""
        try:
            if commodity_name not in self.commodities:
                return False, "Commodity not found!"
            
            if commodity_name not in player.investments:
                return False, "You don't own any of this commodity!"
            
            owned_amount = player.investments[commodity_name]["amount"]
            if owned_amount < amount:
                return False, f"You only own {owned_amount} {commodity_name}!"
            
            # Execute sale
            commodity = self.commodities[commodity_name]
            total_value = commodity["price"] * amount
            
            player.gold += total_value
            player.investments[commodity_name]["amount"] -= amount
            
            # Remove investment if amount reaches 0
            if player.investments[commodity_name]["amount"] <= 0:
                del player.investments[commodity_name]
            
            return True, f"Sold {amount} {commodity_name} for {total_value:.2f} gold!"
            
        except Exception as e:
            print(f"Error selling commodity: {e}")
            return False, "Error processing sale!"
    
    def get_portfolio_value(self, player):
        """Calculate total portfolio value"""
        try:
            total_value = 0
            
            for commodity_name, investment in player.investments.items():
                if commodity_name in self.commodities:
                    current_price = self.commodities[commodity_name]["price"]
                    amount = investment["amount"]
                    total_value += current_price * amount
            
            return total_value
            
        except Exception as e:
            print(f"Error calculating portfolio value: {e}")
            return 0
    
    def get_portfolio_profit_loss(self, player):
        """Calculate profit/loss for portfolio"""
        try:
            total_invested = 0
            current_value = 0
            
            for commodity_name, investment in player.investments.items():
                if commodity_name in self.commodities:
                    avg_price = investment["avg_price"]
                    amount = investment["amount"]
                    current_price = self.commodities[commodity_name]["price"]
                    
                    total_invested += avg_price * amount
                    current_value += current_price * amount
            
            profit_loss = current_value - total_invested
            profit_loss_percent = (profit_loss / total_invested * 100) if total_invested > 0 else 0
            
            return profit_loss, profit_loss_percent
            
        except Exception as e:
            print(f"Error calculating profit/loss: {e}")
            return 0, 0
    
    def show_market_status(self):
        """Display current market status"""
        try:
            print("\n📊 STOCK MARKET STATUS")
            print("=" * 40)
            
            for name, commodity in self.commodities.items():
                price = commodity["price"]
                trend = commodity["trend"]
                
                # Trend indicator
                if trend > 0.3:
                    trend_indicator = "📈 Bullish"
                elif trend < -0.3:
                    trend_indicator = "📉 Bearish"
                else:
                    trend_indicator = "➡️ Stable"
                
                # Price history for trend
                if len(self.price_history[name]) >= 2:
                    price_change = price - self.price_history[name][-2]
                    change_percent = (price_change / self.price_history[name][-2]) * 100
                    
                    if price_change > 0:
                        change_str = f"📈 +{price_change:.2f} (+{change_percent:.1f}%)"
                    elif price_change < 0:
                        change_str = f"📉 {price_change:.2f} ({change_percent:.1f}%)"
                    else:
                        change_str = "➡️ No change"
                else:
                    change_str = "➡️ No data"
                
                print(f"{name:15} | {price:8.2f} gold | {trend_indicator:12} | {change_str}")
            
            # Show recent market events
            if self.market_events:
                print(f"\n📰 RECENT MARKET NEWS:")
                for event_data in self.market_events[-3:]:  # Show last 3 events
                    print(f"  • {event_data['event']}")
            
        except Exception as e:
            print(f"Error showing market status: {e}")
    
    def show_portfolio(self, player):
        """Display player's investment portfolio"""
        try:
            print(f"\n💼 INVESTMENT PORTFOLIO")
            print("=" * 50)
            
            if not player.investments:
                print("📭 No investments yet!")
                return
            
            total_value = 0
            total_invested = 0
            
            print(f"{'Commodity':<15} | {'Amount':<8} | {'Avg Price':<10} | {'Current':<10} | {'Value':<10} | {'P/L':<12}")
            print("-" * 80)
            
            for commodity_name, investment in player.investments.items():
                if commodity_name in self.commodities:
                    amount = investment["amount"]
                    avg_price = investment["avg_price"]
                    current_price = self.commodities[commodity_name]["price"]
                    
                    current_value = current_price * amount
                    invested_value = avg_price * amount
                    profit_loss = current_value - invested_value
                    profit_loss_percent = (profit_loss / invested_value * 100) if invested_value > 0 else 0
                    
                    total_value += current_value
                    total_invested += invested_value
                    
                    # Color coding for profit/loss
                    if profit_loss > 0:
                        pl_str = f"📈 +{profit_loss:.2f} (+{profit_loss_percent:.1f}%)"
                    elif profit_loss < 0:
                        pl_str = f"📉 {profit_loss:.2f} ({profit_loss_percent:.1f}%)"
                    else:
                        pl_str = f"➡️ {profit_loss:.2f} (0.0%)"
                    
                    print(f"{commodity_name:<15} | {amount:<8.1f} | {avg_price:<10.2f} | {current_price:<10.2f} | {current_value:<10.2f} | {pl_str}")
            
            print("-" * 80)
            total_profit_loss = total_value - total_invested
            total_pl_percent = (total_profit_loss / total_invested * 100) if total_invested > 0 else 0
            
            print(f"💰 Total Portfolio Value: {total_value:.2f} gold")
            print(f"💸 Total Invested: {total_invested:.2f} gold")
            
            if total_profit_loss > 0:
                print(f"📈 Total Profit: +{total_profit_loss:.2f} gold (+{total_pl_percent:.1f}%)")
            elif total_profit_loss < 0:
                print(f"📉 Total Loss: {total_profit_loss:.2f} gold ({total_pl_percent:.1f}%)")
            else:
                print(f"➡️ Break Even: {total_profit_loss:.2f} gold (0.0%)")
            
        except Exception as e:
            print(f"Error showing portfolio: {e}")
    
    def get_market_data(self):
        """Get market data for saving"""
        try:
            return {
                "commodities": self.commodities,
                "price_history": self.price_history,
                "market_events": self.market_events,
                "last_update": self.last_update
            }
        except Exception as e:
            print(f"Error getting market data: {e}")
            return {}
    
    def load_market_data(self, data):
        """Load market data from save"""
        try:
            self.commodities = data.get("commodities", {})
            self.price_history = data.get("price_history", {})
            self.market_events = data.get("market_events", [])
            self.last_update = data.get("last_update", time.time())
            
            # Ensure all required commodities exist
            for name, initial_data in Config.INITIAL_COMMODITIES.items():
                if name not in self.commodities:
                    self.commodities[name] = {
                        "price": initial_data["price"],
                        "volatility": initial_data["volatility"],
                        "trend": 0.0,
                        "volume": random.randint(100, 1000)
                    }
                    self.price_history[name] = [initial_data["price"]]
            
            return True
            
        except Exception as e:
            print(f"Error loading market data: {e}")
            return False
