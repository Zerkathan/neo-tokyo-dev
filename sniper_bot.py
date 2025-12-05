#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔴 SNIPER BOT - Opportunity Hunter & Change Monitor                        ║
║  24/7 monitoring with instant Telegram/Discord alerts                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import json
import re
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

import aiohttp
from bs4 import BeautifulSoup


# ══════════════════════════════════════════════════════════════════════════════
# 🎨 NEON COLORS
# ══════════════════════════════════════════════════════════════════════════════

class NeonColors:
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# ══════════════════════════════════════════════════════════════════════════════
# 📊 DATA STRUCTURES
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class Target:
    """Monitoring target configuration."""
    name: str
    url: str
    selector: str
    change_type: str  # 'price_drop', 'stock_available', 'content_change', 'new_listing'
    threshold: Optional[float] = None
    check_interval: int = 60
    telegram_chat_id: Optional[str] = None
    discord_webhook: Optional[str] = None
    enabled: bool = True


# ══════════════════════════════════════════════════════════════════════════════
# 💾 DATABASE
# ══════════════════════════════════════════════════════════════════════════════

class SniperDB:
    """SQLite database for change history."""
    
    def __init__(self, db_path: str = "sniper_history.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_name TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                old_value TEXT,
                new_value TEXT,
                change_type TEXT,
                notified BOOLEAN DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_target_timestamp 
            ON changes(target_name, timestamp DESC)
        ''')
        
        conn.commit()
        conn.close()
    
    def get_last_value(self, target_name: str) -> Optional[str]:
        """Get last recorded value for target."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT new_value FROM changes
            WHERE target_name = ?
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (target_name,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def log_change(self, target_name: str, old_value: str, new_value: str, change_type: str, notified: bool = False):
        """Log a detected change."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO changes (target_name, timestamp, old_value, new_value, change_type, notified)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (target_name, datetime.now().isoformat(), old_value, new_value, change_type, notified))
        
        conn.commit()
        conn.close()
    
    def get_stats(self) -> Dict:
        """Get monitoring statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM changes')
        total_changes = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM changes WHERE notified = 1')
        notified = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_changes': total_changes,
            'notified': notified
        }


# ══════════════════════════════════════════════════════════════════════════════
# 🔍 CHANGE DETECTORS
# ══════════════════════════════════════════════════════════════════════════════

class ChangeDetector:
    """Detect different types of changes."""
    
    @staticmethod
    def extract_price(text: str) -> Optional[float]:
        """Extract price from text."""
        # Patterns: $100, $1,000.50, USD 100, 100.00, etc.
        patterns = [
            r'\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:USD|EUR|GBP)?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                price_str = match.group(1).replace(',', '')
                try:
                    return float(price_str)
                except:
                    continue
        
        return None
    
    @staticmethod
    def detect_price_drop(old_value: str, new_value: str, threshold: float = 0.0) -> bool:
        """Detect if price dropped below threshold percentage."""
        old_price = ChangeDetector.extract_price(old_value)
        new_price = ChangeDetector.extract_price(new_value)
        
        if old_price and new_price:
            change_percent = ((new_price - old_price) / old_price) * 100
            return change_percent < -threshold
        
        return False
    
    @staticmethod
    def detect_stock_available(old_value: str, new_value: str) -> bool:
        """Detect if product came back in stock."""
        out_of_stock_indicators = ['out of stock', 'sold out', 'unavailable', 'not available']
        in_stock_indicators = ['add to cart', 'buy now', 'in stock', 'available']
        
        old_lower = old_value.lower() if old_value else ""
        new_lower = new_value.lower() if new_value else ""
        
        was_unavailable = any(indicator in old_lower for indicator in out_of_stock_indicators)
        is_available = any(indicator in new_lower for indicator in in_stock_indicators)
        
        return was_unavailable and is_available
    
    @staticmethod
    def detect_content_change(old_value: str, new_value: str) -> bool:
        """Detect if content changed."""
        if not old_value or not new_value:
            return False
        
        # Use hash to detect changes
        old_hash = hashlib.md5(old_value.encode()).hexdigest()
        new_hash = hashlib.md5(new_value.encode()).hexdigest()
        
        return old_hash != new_hash


# ══════════════════════════════════════════════════════════════════════════════
# 📱 NOTIFICATIONS
# ══════════════════════════════════════════════════════════════════════════════

class Notifier:
    """Send notifications to Telegram and Discord."""
    
    @staticmethod
    async def send_telegram(chat_id: str, token: str, message: str) -> bool:
        """Send message via Telegram Bot API."""
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json={
                    'chat_id': chat_id,
                    'text': message,
                    'parse_mode': 'Markdown'
                }, timeout=10) as resp:
                    return resp.status == 200
        except Exception as e:
            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Telegram failed: {e}")
            return False
    
    @staticmethod
    async def send_discord(webhook_url: str, message: str) -> bool:
        """Send message via Discord Webhook."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json={
                    'content': message
                }, timeout=10) as resp:
                    return resp.status in [200, 204]
        except Exception as e:
            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Discord failed: {e}")
            return False
    
    @staticmethod
    def format_alert(target: Target, old_value: str, new_value: str, change_type: str) -> str:
        """Format alert message with emojis."""
        emojis = {
            'price_drop': '💰📉',
            'stock_available': '🛒✅',
            'content_change': '📝🔄',
            'new_listing': '🆕⚡'
        }
        
        emoji = emojis.get(change_type, '🔔')
        
        message = f"{emoji} **ALERT: {target.name}**\n\n"
        message += f"🔗 URL: {target.url}\n"
        message += f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if change_type == 'price_drop':
            old_price = ChangeDetector.extract_price(old_value)
            new_price = ChangeDetector.extract_price(new_value)
            if old_price and new_price:
                change = ((new_price - old_price) / old_price) * 100
                message += f"💵 Old Price: ${old_price:,.2f}\n"
                message += f"💰 New Price: ${new_price:,.2f}\n"
                message += f"📊 Change: {change:.1f}%\n"
        elif change_type == 'stock_available':
            message += f"✅ Product is now IN STOCK!\n"
        else:
            message += f"📝 Old: {old_value[:100]}...\n"
            message += f"📝 New: {new_value[:100]}...\n"
        
        return message


# ══════════════════════════════════════════════════════════════════════════════
# 🎯 SNIPER BOT
# ══════════════════════════════════════════════════════════════════════════════

class SniperBot:
    """Main monitoring bot."""
    
    def __init__(self, config_path: str = "sniper_config.json"):
        self.config_path = config_path
        self.targets = []
        self.db = SniperDB()
        self.telegram_token = None
        self.load_config()
    
    def load_config(self):
        """Load configuration from file."""
        config_file = Path(self.config_path)
        
        if not config_file.exists():
            print(f"{NeonColors.YELLOW}[WARN]{NeonColors.RESET} Config not found, creating default...")
            self.create_default_config()
            return
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
                self.telegram_token = config.get('telegram_token')
                
                self.targets = [
                    Target(**target_data) 
                    for target_data in config.get('targets', [])
                ]
                
                print(f"{NeonColors.GREEN}[LOADED]{NeonColors.RESET} Config: {len(self.targets)} targets")
        except Exception as e:
            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Failed to load config: {e}")
    
    def create_default_config(self):
        """Create default configuration file."""
        default = {
            "telegram_token": "YOUR_BOT_TOKEN_HERE",
            "targets": [
                {
                    "name": "Example Product",
                    "url": "https://example.com/product",
                    "selector": ".price",
                    "change_type": "price_drop",
                    "threshold": 5.0,
                    "check_interval": 60,
                    "telegram_chat_id": "YOUR_CHAT_ID",
                    "discord_webhook": None,
                    "enabled": False
                }
            ]
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(default, f, indent=2)
        
        print(f"{NeonColors.GREEN}[CREATED]{NeonColors.RESET} {self.config_path}")
        print(f"{NeonColors.YELLOW}[INFO]{NeonColors.RESET} Please edit config with your settings")
    
    async def check_target(self, target: Target) -> Optional[Dict]:
        """Check a single target for changes."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(target.url, timeout=10) as resp:
                    if resp.status != 200:
                        print(f"{NeonColors.RED}[{resp.status}]{NeonColors.RESET} {target.name}")
                        return None
                    
                    html = await resp.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract content
                    element = soup.select_one(target.selector)
                    if not element:
                        print(f"{NeonColors.YELLOW}[WARN]{NeonColors.RESET} Selector not found: {target.name}")
                        return None
                    
                    current_value = element.get_text(strip=True)
                    
                    # Get previous value
                    previous_value = self.db.get_last_value(target.name)
                    
                    # First run - just record
                    if not previous_value:
                        self.db.log_change(target.name, None, current_value, target.change_type, False)
                        print(f"{NeonColors.CYAN}[INIT]{NeonColors.RESET} {target.name}: {current_value[:50]}...")
                        return None
                    
                    # Detect change
                    change_detected = False
                    
                    if target.change_type == 'price_drop':
                        change_detected = ChangeDetector.detect_price_drop(
                            previous_value, current_value, target.threshold or 0
                        )
                    elif target.change_type == 'stock_available':
                        change_detected = ChangeDetector.detect_stock_available(
                            previous_value, current_value
                        )
                    elif target.change_type == 'content_change':
                        change_detected = ChangeDetector.detect_content_change(
                            previous_value, current_value
                        )
                    
                    if change_detected:
                        print(f"{NeonColors.RED}[CHANGE!]{NeonColors.RESET} {target.name}")
                        
                        # Log change
                        self.db.log_change(target.name, previous_value, current_value, target.change_type, True)
                        
                        return {
                            'target': target,
                            'old_value': previous_value,
                            'new_value': current_value
                        }
                    else:
                        print(f"{NeonColors.GREEN}[OK]{NeonColors.RESET} {target.name}: No change")
                        
                        # Update value if it changed but didn't trigger alert
                        if previous_value != current_value:
                            self.db.log_change(target.name, previous_value, current_value, target.change_type, False)
                    
                    return None
                    
        except asyncio.TimeoutError:
            print(f"{NeonColors.YELLOW}[TIMEOUT]{NeonColors.RESET} {target.name}")
        except Exception as e:
            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} {target.name}: {e}")
        
        return None
    
    async def send_alert(self, change_data: Dict):
        """Send alert for detected change."""
        target = change_data['target']
        old_value = change_data['old_value']
        new_value = change_data['new_value']
        
        message = Notifier.format_alert(target, old_value, new_value, target.change_type)
        
        alerts_sent = []
        
        # Send Telegram
        if target.telegram_chat_id and self.telegram_token:
            success = await Notifier.send_telegram(
                target.telegram_chat_id,
                self.telegram_token,
                message
            )
            if success:
                alerts_sent.append('Telegram')
                print(f"{NeonColors.GREEN}[SENT]{NeonColors.RESET} Telegram alert")
        
        # Send Discord
        if target.discord_webhook:
            success = await Notifier.send_discord(
                target.discord_webhook,
                message
            )
            if success:
                alerts_sent.append('Discord')
                print(f"{NeonColors.GREEN}[SENT]{NeonColors.RESET} Discord alert")
        
        if not alerts_sent:
            print(f"{NeonColors.YELLOW}[WARN]{NeonColors.RESET} No notification channels configured")
    
    async def run_check_cycle(self):
        """Run one check cycle for all targets."""
        enabled_targets = [t for t in self.targets if t.enabled]
        
        if not enabled_targets:
            print(f"{NeonColors.YELLOW}[WARN]{NeonColors.RESET} No enabled targets")
            return
        
        print(f"{NeonColors.CYAN}[CHECK]{NeonColors.RESET} Checking {len(enabled_targets)} targets...")
        
        # Check all targets in parallel
        tasks = [self.check_target(target) for target in enabled_targets]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Send alerts for detected changes
        for result in results:
            if isinstance(result, dict):
                await self.send_alert(result)
    
    async def run_continuous(self, interval: int = 60):
        """Run continuous monitoring."""
        print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
        print(f"{NeonColors.BOLD}{NeonColors.RED}🔴 SNIPER BOT - Starting continuous monitoring{NeonColors.RESET}")
        print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
        
        print(f"{NeonColors.YELLOW}[CONFIG]{NeonColors.RESET} Targets: {len(self.targets)}")
        print(f"{NeonColors.YELLOW}[CONFIG]{NeonColors.RESET} Interval: {interval}s")
        print(f"{NeonColors.GREEN}[START]{NeonColors.RESET} Monitoring started. Press Ctrl+C to stop\n")
        
        cycle = 0
        
        try:
            while True:
                cycle += 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                print(f"{NeonColors.CYAN}{'─' * 78}{NeonColors.RESET}")
                print(f"{NeonColors.BOLD}[CYCLE #{cycle}]{NeonColors.RESET} {timestamp}")
                print(f"{NeonColors.CYAN}{'─' * 78}{NeonColors.RESET}\n")
                
                await self.run_check_cycle()
                
                print(f"\n{NeonColors.BLUE}[SLEEP]{NeonColors.RESET} Next check in {interval}s...\n")
                await asyncio.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n\n{NeonColors.YELLOW}[STOP]{NeonColors.RESET} Monitoring stopped")
            print(f"{NeonColors.GREEN}[STATS]{NeonColors.RESET} Total cycles: {cycle}\n")
    
    def show_stats(self):
        """Display monitoring statistics."""
        stats = self.db.get_stats()
        
        print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
        print(f"{NeonColors.BOLD}{NeonColors.MAGENTA}📊 SNIPER BOT STATISTICS{NeonColors.RESET}")
        print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
        
        print(f"{NeonColors.YELLOW}Total Targets:{NeonColors.RESET} {len(self.targets)}")
        print(f"{NeonColors.YELLOW}Enabled:{NeonColors.RESET} {sum(1 for t in self.targets if t.enabled)}")
        print(f"{NeonColors.YELLOW}Total Changes Detected:{NeonColors.RESET} {stats['total_changes']}")
        print(f"{NeonColors.YELLOW}Alerts Sent:{NeonColors.RESET} {stats['notified']}")
        
        print(f"\n{NeonColors.GREEN}Configured Targets:{NeonColors.RESET}")
        for i, target in enumerate(self.targets, 1):
            status = f"{NeonColors.GREEN}✓{NeonColors.RESET}" if target.enabled else f"{NeonColors.RED}✗{NeonColors.RESET}"
            print(f"  {status} {target.name} ({target.change_type})")
        
        print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")


# ══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN CLI
# ══════════════════════════════════════════════════════════════════════════════

def print_help():
    """Print usage help."""
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.RED}🔴 SNIPER BOT - Usage{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
    
    print(f"{NeonColors.GREEN}Commands:{NeonColors.RESET}\n")
    print(f"  {NeonColors.YELLOW}run{NeonColors.RESET}                Start continuous monitoring")
    print(f"  {NeonColors.YELLOW}check{NeonColors.RESET}              Run single check cycle")
    print(f"  {NeonColors.YELLOW}stats{NeonColors.RESET}             Show statistics")
    print(f"  {NeonColors.YELLOW}help{NeonColors.RESET}              Show this help")
    
    print(f"\n{NeonColors.GREEN}Examples:{NeonColors.RESET}\n")
    print(f"  {NeonColors.CYAN}python sniper_bot.py run{NeonColors.RESET}")
    print(f"  {NeonColors.CYAN}python sniper_bot.py check{NeonColors.RESET}")
    print(f"  {NeonColors.CYAN}python sniper_bot.py stats{NeonColors.RESET}")
    
    print(f"\n{NeonColors.YELLOW}[NOTE]{NeonColors.RESET} Configure targets in: sniper_config.json")
    print(f"{NeonColors.YELLOW}[NOTE]{NeonColors.RESET} Get Telegram bot token: @BotFather on Telegram")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")


def main():
    """Main CLI entry point."""
    import sys
    
    bot = SniperBot()
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "run":
        asyncio.run(bot.run_continuous(interval=60))
    
    elif command == "check":
        asyncio.run(bot.run_check_cycle())
    
    elif command == "stats":
        bot.show_stats()
    
    elif command == "help":
        print_help()
    
    else:
        print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Unknown command: {command}")
        print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{NeonColors.YELLOW}[EXIT]{NeonColors.RESET} Terminated\n")
    except Exception as e:
        print(f"\n{NeonColors.RED}[FATAL]{NeonColors.RESET} {e}\n")

