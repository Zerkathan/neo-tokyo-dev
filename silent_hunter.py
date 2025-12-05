#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🎯 SILENT HUNTER - Focused Price & Stock Monitor                           ║
║  Single-target monitoring with Telegram alerts - Production version         ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROJECT: Silent Hunter
PURPOSE: Monitor ONE product/URL for price drops or stock availability
ALERT: Instant Telegram notification when change detected
"""

import os
import time
import random
import logging
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
from datetime import datetime


# ══════════════════════════════════════════════════════════════════════════════
# ⚙️ CONFIGURATION (Edit these values)
# ══════════════════════════════════════════════════════════════════════════════

# Target URL to monitor
TARGET_URL = "https://www.amazon.com/dp/B0B16YLLH7"  # Example: RTX 4090

# CSS selector for price element
PRICE_SELECTOR = "span.a-price-whole"

# CSS selector for stock/availability
STOCK_SELECTOR = "#availability span"

# Alert when price drops below this value (USD)
TARGET_PRICE = 1500.0

# Telegram credentials (GET THESE FIRST!)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")

# Check interval (seconds)
CHECK_INTERVAL = 60

# Enable detailed logging
VERBOSE = True


# ══════════════════════════════════════════════════════════════════════════════
# 🎨 LOGGING SETUP
# ══════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO if VERBOSE else logging.WARNING,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# 🕵️ USER AGENT ROTATION
# ══════════════════════════════════════════════════════════════════════════════

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
]


def get_random_user_agent() -> str:
    """Return a random User-Agent to avoid detection."""
    return random.choice(USER_AGENTS)


# ══════════════════════════════════════════════════════════════════════════════
# 🎯 PRODUCT MONITOR CLASS
# ══════════════════════════════════════════════════════════════════════════════

class ProductMonitor:
    """
    Robust product price and stock monitor.
    
    Features:
    - User-Agent rotation
    - Exponential backoff on errors
    - Price extraction and validation
    - Stock availability checking
    - Telegram alert integration
    """
    
    def __init__(
        self,
        url: str,
        price_selector: str,
        stock_selector: str,
        target_price: float,
        telegram_token: str,
        telegram_chat_id: str
    ):
        """
        Initialize product monitor.
        
        Args:
            url: Product URL to monitor
            price_selector: CSS selector for price element
            stock_selector: CSS selector for stock/availability element
            target_price: Alert when price drops below this
            telegram_token: Telegram bot API token
            telegram_chat_id: Your Telegram chat ID
        """
        self.url = url
        self.price_selector = price_selector
        self.stock_selector = stock_selector
        self.target_price = target_price
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        
        self.last_price: Optional[float] = None
        self.last_stock_status: Optional[str] = None
        self.retry_count = 0
        self.max_retries = 5
    
    def fetch_page(self) -> Optional[str]:
        """
        Fetch webpage with robust error handling and exponential backoff.
        
        Returns:
            HTML content or None if failed
        """
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        try:
            logger.info(f"🔍 Fetching: {self.url[:50]}...")
            
            response = requests.get(
                self.url,
                headers=headers,
                timeout=15,
                allow_redirects=True
            )
            
            response.raise_for_status()
            self.retry_count = 0  # Reset on success
            
            logger.info(f"✅ Status: {response.status_code}")
            return response.text
            
        except requests.exceptions.Timeout:
            logger.error("⏱️ Timeout - Site too slow")
            return self._handle_fetch_error()
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"🚫 HTTP Error: {e}")
            return self._handle_fetch_error()
            
        except requests.exceptions.ConnectionError:
            logger.error("🔌 Connection Error - Site down?")
            return self._handle_fetch_error()
            
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return self._handle_fetch_error()
    
    def _handle_fetch_error(self) -> None:
        """Handle fetch errors with exponential backoff."""
        self.retry_count += 1
        
        if self.retry_count >= self.max_retries:
            logger.error(f"💀 Max retries ({self.max_retries}) reached. Giving up.")
            self.retry_count = 0
            return None
        
        # Exponential backoff: 2^retry_count seconds
        backoff_time = 2 ** self.retry_count
        logger.warning(f"⏳ Retry {self.retry_count}/{self.max_retries} in {backoff_time}s...")
        time.sleep(backoff_time)
        
        return None
    
    def extract_price(self, html: str) -> Optional[float]:
        """
        Extract price from HTML using selector.
        
        Args:
            html: Page HTML content
            
        Returns:
            Price as float or None if not found
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            price_element = soup.select_one(self.price_selector)
            
            if not price_element:
                logger.warning(f"⚠️ Price element not found (selector: {self.price_selector})")
                return None
            
            # Extract text and clean
            price_text = price_element.get_text(strip=True)
            
            # Remove currency symbols and commas
            price_clean = price_text.replace('$', '').replace(',', '').replace('€', '').replace('£', '')
            
            # Extract first number
            import re
            match = re.search(r'(\d+\.?\d*)', price_clean)
            if match:
                price = float(match.group(1))
                logger.info(f"💰 Price extracted: ${price:.2f}")
                return price
            else:
                logger.warning(f"⚠️ Could not parse price from: {price_text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Price extraction failed: {e}")
            return None
    
    def validate_stock(self, html: str) -> bool:
        """
        Check if product is in stock.
        
        Args:
            html: Page HTML content
            
        Returns:
            True if in stock, False otherwise
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            stock_element = soup.select_one(self.stock_selector)
            
            if not stock_element:
                logger.warning(f"⚠️ Stock element not found (selector: {self.stock_selector})")
                return False
            
            stock_text = stock_element.get_text(strip=True).lower()
            
            # Check for in-stock indicators
            in_stock_keywords = ['in stock', 'available', 'add to cart', 'buy now']
            out_of_stock_keywords = ['out of stock', 'unavailable', 'sold out', 'notify me']
            
            is_available = any(keyword in stock_text for keyword in in_stock_keywords)
            is_unavailable = any(keyword in stock_text for keyword in out_of_stock_keywords)
            
            if is_unavailable:
                logger.info("📦 Stock: OUT OF STOCK")
                return False
            elif is_available:
                logger.info("✅ Stock: AVAILABLE")
                return True
            else:
                logger.info(f"❓ Stock: Unknown ({stock_text})")
                return False
                
        except Exception as e:
            logger.error(f"❌ Stock validation failed: {e}")
            return False
    
    def send_alert(self, message: str) -> bool:
        """
        Send alert to Telegram.
        
        Args:
            message: Alert message to send
            
        Returns:
            True if sent successfully, False otherwise
        """
        if self.telegram_token == "YOUR_BOT_TOKEN_HERE":
            logger.warning("⚠️ Telegram not configured. Set TELEGRAM_TOKEN and TELEGRAM_CHAT_ID")
            print(f"\n📱 ALERT (would send to Telegram):\n{message}\n")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            
            payload = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info("📨 Telegram alert sent!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Telegram send failed: {e}")
            return False
    
    def check(self) -> bool:
        """
        Main check method - fetches page, extracts data, triggers alerts if needed.
        
        Returns:
            True if check completed successfully, False otherwise
        """
        # Fetch page
        html = self.fetch_page()
        if not html:
            return False
        
        # Extract price
        current_price = self.extract_price(html)
        
        # Check stock
        is_in_stock = self.validate_stock(html)
        
        # Detect changes and send alerts
        alerts_sent = []
        
        # Price drop alert
        if current_price and current_price <= self.target_price:
            if self.last_price is None or current_price < self.last_price:
                message = (
                    f"🎯💰 **PRICE ALERT!**\n\n"
                    f"💵 Current Price: **${current_price:.2f}**\n"
                    f"🎯 Target Price: ${self.target_price:.2f}\n"
                    f"📊 Status: {'✅ BELOW TARGET!' if current_price <= self.target_price else '⚠️ Above target'}\n\n"
                    f"🔗 [View Product]({self.url})\n"
                    f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                
                if self.send_alert(message):
                    alerts_sent.append("Price Drop")
        
        # Stock availability alert
        if is_in_stock and (self.last_stock_status is None or not self.last_stock_status):
            message = (
                f"🛒✅ **STOCK ALERT!**\n\n"
                f"✅ Product is now **IN STOCK**!\n"
                f"💰 Price: ${current_price:.2f if current_price else 'N/A'}\n\n"
                f"🔗 [BUY NOW]({self.url})\n"
                f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            
            if self.send_alert(message):
                alerts_sent.append("Stock Available")
        
        # Update state
        if current_price:
            self.last_price = current_price
        self.last_stock_status = is_in_stock
        
        # Summary
        if alerts_sent:
            logger.info(f"🚨 ALERTS SENT: {', '.join(alerts_sent)}")
        
        return True
    
    def run_continuous(self):
        """
        Run continuous monitoring loop.
        
        Checks every CHECK_INTERVAL seconds until Ctrl+C.
        """
        print("\n" + "═" * 78)
        print("🎯 SILENT HUNTER - Starting Monitoring")
        print("═" * 78 + "\n")
        
        print(f"🔗 Target: {self.url}")
        print(f"💰 Target Price: ${self.target_price:.2f}")
        print(f"⏱️ Check Interval: {CHECK_INTERVAL}s")
        print(f"📱 Telegram: {'✅ Configured' if self.telegram_token != 'YOUR_BOT_TOKEN_HERE' else '❌ Not configured'}")
        print(f"\n🟢 Monitoring started. Press Ctrl+C to stop.\n")
        print("─" * 78 + "\n")
        
        cycle = 0
        
        try:
            while True:
                cycle += 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                print(f"[CYCLE #{cycle}] {timestamp}")
                print("─" * 40)
                
                success = self.check()
                
                if success:
                    print("✅ Check complete\n")
                else:
                    print("❌ Check failed\n")
                
                print(f"⏳ Waiting {CHECK_INTERVAL}s until next check...\n")
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")
            print(f"📊 Total cycles completed: {cycle}")
            print("👋 Silent Hunter terminated\n")


# ══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point."""
    # Validate configuration
    if TELEGRAM_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("\n⚠️  WARNING: Telegram not configured!")
        print("📱 Get your bot token from @BotFather on Telegram")
        print("🆔 Get your chat ID from @userinfobot on Telegram")
        print("⚙️  Set environment variables:")
        print("   export TELEGRAM_TOKEN='your_bot_token'")
        print("   export TELEGRAM_CHAT_ID='your_chat_id'")
        print("\n💡 Or edit the script directly (lines 31-32)")
        print("\n🔄 Running in demo mode (alerts will print to console)...\n")
    
    # Create monitor
    monitor = ProductMonitor(
        url=TARGET_URL,
        price_selector=PRICE_SELECTOR,
        stock_selector=STOCK_SELECTOR,
        target_price=TARGET_PRICE,
        telegram_token=TELEGRAM_TOKEN,
        telegram_chat_id=TELEGRAM_CHAT_ID
    )
    
    # Run
    monitor.run_continuous()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"💀 Fatal error: {e}")
        print(f"\n❌ Silent Hunter crashed: {e}\n")

