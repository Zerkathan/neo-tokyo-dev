#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🎮 COMMAND CENTER - Personal Dashboard CLI                                 ║
║  Your morning briefing in one Cyberpunk terminal screen                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import json
import aiohttp
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from abc import ABC, abstractmethod


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
# ⚙️ CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

DEFAULT_CONFIG = {
    "user_location": "New York",
    "crypto_holdings": {
        "bitcoin": 0.1,
        "ethereum": 1.5,
        "solana": 50
    },
    "server_urls": [
        "https://google.com",
        "https://github.com",
        "https://stackoverflow.com"
    ],
    "news_sources": ["hacker_news"],
    "todo_file": "todos.txt"
}


def load_config() -> Dict:
    """Load configuration from config.json or use defaults."""
    config_path = Path("config.json")
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            pass
    
    return DEFAULT_CONFIG


# ══════════════════════════════════════════════════════════════════════════════
# 📦 BASE MODULE
# ══════════════════════════════════════════════════════════════════════════════

class DashboardModule(ABC):
    """Base class for dashboard modules."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.data = None
        self.error = None
    
    @abstractmethod
    async def fetch_data(self):
        """Fetch data asynchronously."""
        pass
    
    @abstractmethod
    def render(self) -> str:
        """Render module output."""
        pass


# ══════════════════════════════════════════════════════════════════════════════
# 📰 NEWS MODULE
# ══════════════════════════════════════════════════════════════════════════════

class NewsModule(DashboardModule):
    """Fetch and display tech news."""
    
    async def fetch_data(self):
        """Fetch top news from Hacker News."""
        try:
            async with aiohttp.ClientSession() as session:
                # Get top stories
                async with session.get('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=5) as resp:
                    if resp.status == 200:
                        story_ids = await resp.json()
                        
                        # Fetch top 5 stories
                        stories = []
                        for story_id in story_ids[:5]:
                            try:
                                async with session.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json', timeout=3) as story_resp:
                                    if story_resp.status == 200:
                                        story = await story_resp.json()
                                        stories.append(story)
                            except:
                                continue
                        
                        self.data = stories
        except Exception as e:
            self.error = str(e)
    
    def render(self) -> str:
        """Render news panel."""
        output = f"{NeonColors.MAGENTA}{'═' * 38}{NeonColors.RESET}\n"
        output += f"{NeonColors.BOLD}{NeonColors.CYAN}📰 TECH NEWS (Hacker News){NeonColors.RESET}\n"
        output += f"{NeonColors.MAGENTA}{'═' * 38}{NeonColors.RESET}\n"
        
        if self.error:
            output += f"{NeonColors.RED}Error: {self.error}{NeonColors.RESET}\n"
        elif self.data:
            for i, story in enumerate(self.data, 1):
                title = story.get('title', 'No title')[:32]
                score = story.get('score', 0)
                output += f"{NeonColors.YELLOW}{i}.{NeonColors.RESET} {title}...\n"
                output += f"   {NeonColors.GREEN}▲ {score}{NeonColors.RESET} pts\n"
        else:
            output += f"{NeonColors.YELLOW}Loading...{NeonColors.RESET}\n"
        
        return output


# ══════════════════════════════════════════════════════════════════════════════
# 💰 CRYPTO MODULE
# ══════════════════════════════════════════════════════════════════════════════

class CryptoModule(DashboardModule):
    """Fetch and display cryptocurrency prices."""
    
    async def fetch_data(self):
        """Fetch crypto prices from CoinGecko."""
        try:
            async with aiohttp.ClientSession() as session:
                url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true'
                async with session.get(url, timeout=5) as resp:
                    if resp.status == 200:
                        self.data = await resp.json()
        except Exception as e:
            self.error = str(e)
    
    def render(self) -> str:
        """Render crypto panel."""
        output = f"{NeonColors.MAGENTA}{'═' * 38}{NeonColors.RESET}\n"
        output += f"{NeonColors.BOLD}{NeonColors.YELLOW}💰 CRYPTO PRICES{NeonColors.RESET}\n"
        output += f"{NeonColors.MAGENTA}{'═' * 38}{NeonColors.RESET}\n"
        
        if self.error:
            output += f"{NeonColors.RED}Error: {self.error}{NeonColors.RESET}\n"
        elif self.data:
            holdings = self.config.get('crypto_holdings', {})
            total_value = 0
            
            icons = {'bitcoin': '₿', 'ethereum': 'Ξ', 'solana': '◎'}
            
            for crypto_id in ['bitcoin', 'ethereum', 'solana']:
                if crypto_id in self.data:
                    price = self.data[crypto_id].get('usd', 0)
                    change = self.data[crypto_id].get('usd_24h_change', 0)
                    
                    # Calculate holding value
                    holding = holdings.get(crypto_id, 0)
                    value = price * holding
                    total_value += value
                    
                    # Arrow indicator
                    arrow = "↑" if change >= 0 else "↓"
                    color = NeonColors.GREEN if change >= 0 else NeonColors.RED
                    
                    icon = icons.get(crypto_id, '●')
                    name = crypto_id.capitalize()[:8]
                    
                    output += f"{NeonColors.CYAN}{icon} {name:8s}{NeonColors.RESET} ${price:>8,.2f} "
                    output += f"{color}{arrow} {change:>5.1f}%{NeonColors.RESET}\n"
                    
                    if holding > 0:
                        output += f"   {NeonColors.BLUE}Holdings: {holding:>6.2f} = ${value:>8,.2f}{NeonColors.RESET}\n"
            
            if total_value > 0:
                output += f"{NeonColors.MAGENTA}{'─' * 38}{NeonColors.RESET}\n"
                output += f"{NeonColors.BOLD}Portfolio: ${total_value:>8,.2f}{NeonColors.RESET}\n"
        else:
            output += f"{NeonColors.YELLOW}Loading...{NeonColors.RESET}\n"
        
        return output


# ══════════════════════════════════════════════════════════════════════════════
# 🌤️ WEATHER MODULE
# ══════════════════════════════════════════════════════════════════════════════

class WeatherModule(DashboardModule):
    """Fetch and display weather forecast."""
    
    async def fetch_data(self):
        """Fetch weather from wttr.in (no API key needed)."""
        try:
            location = self.config.get('user_location', 'NewYork')
            async with aiohttp.ClientSession() as session:
                url = f'https://wttr.in/{location}?format=j1'
                async with session.get(url, timeout=5) as resp:
                    if resp.status == 200:
                        self.data = await resp.json()
        except Exception as e:
            self.error = str(e)
    
    def render(self) -> str:
        """Render weather panel."""
        output = f"{NeonColors.MAGENTA}{'═' * 38}{NeonColors.RESET}\n"
        output += f"{NeonColors.BOLD}{NeonColors.BLUE}🌤️ WEATHER{NeonColors.RESET}\n"
        output += f"{NeonColors.MAGENTA}{'═' * 38}{NeonColors.RESET}\n"
        
        if self.error:
            output += f"{NeonColors.RED}Error: {self.error}{NeonColors.RESET}\n"
        elif self.data:
            try:
                current = self.data.get('current_condition', [{}])[0]
                temp_c = current.get('temp_C', 'N/A')
                temp_f = current.get('temp_F', 'N/A')
                desc = current.get('weatherDesc', [{}])[0].get('value', 'N/A')
                
                output += f"{NeonColors.GREEN}Now:{NeonColors.RESET} {temp_c}°C / {temp_f}°F\n"
                output += f"{NeonColors.CYAN}{desc}{NeonColors.RESET}\n\n"
                
                # 3-day forecast
                weather = self.data.get('weather', [])
                for day in weather[:3]:
                    date = day.get('date', 'N/A')
                    max_temp = day.get('maxtempC', 'N/A')
                    min_temp = day.get('mintempC', 'N/A')
                    
                    output += f"{NeonColors.YELLOW}{date}{NeonColors.RESET} {max_temp}°/{min_temp}°C\n"
                
            except Exception as e:
                output += f"{NeonColors.RED}Parse error{NeonColors.RESET}\n"
        else:
            output += f"{NeonColors.YELLOW}Loading...{NeonColors.RESET}\n"
        
        return output


# ══════════════════════════════════════════════════════════════════════════════
# 🖥️ SERVER STATUS MODULE
# ══════════════════════════════════════════════════════════════════════════════

class ServerModule(DashboardModule):
    """Check server/website availability."""
    
    async def fetch_data(self):
        """Ping URLs to check availability."""
        try:
            urls = self.config.get('server_urls', [])
            results = []
            
            async with aiohttp.ClientSession() as session:
                for url in urls:
                    try:
                        start_time = asyncio.get_event_loop().time()
                        async with session.get(url, timeout=5) as resp:
                            elapsed = (asyncio.get_event_loop().time() - start_time) * 1000
                            results.append({
                                'url': url,
                                'status': resp.status,
                                'response_time': elapsed,
                                'up': resp.status < 400
                            })
                    except Exception as e:
                        results.append({
                            'url': url,
                            'status': 0,
                            'response_time': 0,
                            'up': False,
                            'error': str(e)
                        })
            
            self.data = results
        except Exception as e:
            self.error = str(e)
    
    def render(self) -> str:
        """Render server status panel."""
        output = f"{NeonColors.MAGENTA}{'═' * 38}{NeonColors.RESET}\n"
        output += f"{NeonColors.BOLD}{NeonColors.GREEN}🖥️ SERVER STATUS{NeonColors.RESET}\n"
        output += f"{NeonColors.MAGENTA}{'═' * 38}{NeonColors.RESET}\n"
        
        if self.error:
            output += f"{NeonColors.RED}Error: {self.error}{NeonColors.RESET}\n"
        elif self.data:
            for server in self.data:
                url = server['url'].replace('https://', '').replace('http://', '')[:25]
                
                if server['up']:
                    status = f"{NeonColors.GREEN}●{NeonColors.RESET} UP"
                    rt = f"{server['response_time']:.0f}ms"
                else:
                    status = f"{NeonColors.RED}●{NeonColors.RESET} DOWN"
                    rt = "---"
                
                output += f"{status} {NeonColors.CYAN}{url:25s}{NeonColors.RESET} {rt}\n"
        else:
            output += f"{NeonColors.YELLOW}Loading...{NeonColors.RESET}\n"
        
        return output


# ══════════════════════════════════════════════════════════════════════════════
# ✅ TODO MODULE
# ══════════════════════════════════════════════════════════════════════════════

class TodoModule(DashboardModule):
    """Display pending tasks."""
    
    async def fetch_data(self):
        """Read todos from file."""
        try:
            todo_file = Path(self.config.get('todo_file', 'todos.txt'))
            
            if todo_file.exists():
                with open(todo_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    self.data = [line.strip() for line in lines if line.strip()][:5]
            else:
                # Create sample todos
                self.data = [
                    "[ ] Review Neo-Tokyo Dev documentation",
                    "[ ] Test Intelligence Pipeline",
                    "[ ] Deploy dashboards to production",
                    "[x] Complete Boss Fights",
                    "[ ] Share project on GitHub"
                ]
        except Exception as e:
            self.error = str(e)
    
    def render(self) -> str:
        """Render todo panel."""
        output = f"{NeonColors.MAGENTA}{'═' * 38}{NeonColors.RESET}\n"
        output += f"{NeonColors.BOLD}{NeonColors.YELLOW}✅ TODO LIST{NeonColors.RESET}\n"
        output += f"{NeonColors.MAGENTA}{'═' * 38}{NeonColors.RESET}\n"
        
        if self.error:
            output += f"{NeonColors.RED}Error: {self.error}{NeonColors.RESET}\n"
        elif self.data:
            for i, task in enumerate(self.data, 1):
                if '[x]' in task.lower() or '[✓]' in task:
                    color = NeonColors.GREEN
                    icon = "✓"
                else:
                    color = NeonColors.CYAN
                    icon = "○"
                
                task_text = task.replace('[ ]', '').replace('[x]', '').replace('[✓]', '').strip()
                output += f"{color}{icon}{NeonColors.RESET} {task_text[:32]}\n"
        else:
            output += f"{NeonColors.YELLOW}No tasks{NeonColors.RESET}\n"
        
        return output


# ══════════════════════════════════════════════════════════════════════════════
# 📊 STATS MODULE
# ══════════════════════════════════════════════════════════════════════════════

class StatsModule(DashboardModule):
    """Display system stats."""
    
    async def fetch_data(self):
        """Get system stats."""
        try:
            import psutil
            self.data = {
                'cpu': psutil.cpu_percent(interval=0.1),
                'memory': psutil.virtual_memory().percent,
                'disk': psutil.disk_usage('/').percent
            }
        except ImportError:
            self.data = None
    
    def render(self) -> str:
        """Render stats panel."""
        output = f"{NeonColors.MAGENTA}{'═' * 38}{NeonColors.RESET}\n"
        output += f"{NeonColors.BOLD}{NeonColors.RED}📊 SYSTEM{NeonColors.RESET}\n"
        output += f"{NeonColors.MAGENTA}{'═' * 38}{NeonColors.RESET}\n"
        
        if self.data:
            cpu = self.data['cpu']
            mem = self.data['memory']
            disk = self.data['disk']
            
            output += f"{NeonColors.CYAN}CPU:{NeonColors.RESET}  {self._bar(cpu)} {cpu:.0f}%\n"
            output += f"{NeonColors.CYAN}RAM:{NeonColors.RESET}  {self._bar(mem)} {mem:.0f}%\n"
            output += f"{NeonColors.CYAN}Disk:{NeonColors.RESET} {self._bar(disk)} {disk:.0f}%\n"
        else:
            output += f"{NeonColors.YELLOW}Install psutil{NeonColors.RESET}\n"
        
        return output
    
    def _bar(self, percent: float, width: int = 10) -> str:
        """Generate progress bar."""
        filled = int((percent / 100) * width)
        empty = width - filled
        
        if percent < 50:
            color = NeonColors.GREEN
        elif percent < 80:
            color = NeonColors.YELLOW
        else:
            color = NeonColors.RED
        
        return f"{color}{'█' * filled}{'░' * empty}{NeonColors.RESET}"


# ══════════════════════════════════════════════════════════════════════════════
# 🎮 COMMAND CENTER
# ══════════════════════════════════════════════════════════════════════════════

class CommandCenter:
    """Main dashboard orchestrator."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.modules = [
            NewsModule(config),
            CryptoModule(config),
            WeatherModule(config),
            ServerModule(config),
            TodoModule(config),
            StatsModule(config),
        ]
    
    async def fetch_all(self):
        """Fetch data from all modules in parallel."""
        tasks = [module.fetch_data() for module in self.modules]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    def render_dashboard(self):
        """Render complete dashboard."""
        # Clear screen
        print("\033[2J\033[H", end='')
        
        # Header
        print(f"\n{NeonColors.CYAN}{'╔' + '═' * 78 + '╗'}{NeonColors.RESET}")
        print(f"{NeonColors.CYAN}║{NeonColors.RESET}{NeonColors.BOLD}{NeonColors.MAGENTA}{'🎮 COMMAND CENTER':^78s}{NeonColors.RESET}{NeonColors.CYAN}║{NeonColors.RESET}")
        print(f"{NeonColors.CYAN}║{NeonColors.RESET}{NeonColors.GREEN}{'Personal Dashboard CLI | Neo-Tokyo Dev v3.0':^78s}{NeonColors.RESET}{NeonColors.CYAN}║{NeonColors.RESET}")
        print(f"{NeonColors.CYAN}{'╚' + '═' * 78 + '╝'}{NeonColors.RESET}\n")
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{NeonColors.YELLOW}Last Updated:{NeonColors.RESET} {timestamp}\n")
        
        # Render modules in 2x3 grid
        modules = self.modules
        
        # Row 1: News + Crypto
        lines_news = modules[0].render().split('\n')
        lines_crypto = modules[1].render().split('\n')
        max_lines = max(len(lines_news), len(lines_crypto))
        
        for i in range(max_lines):
            left = lines_news[i] if i < len(lines_news) else ' ' * 38
            right = lines_crypto[i] if i < len(lines_crypto) else ' ' * 38
            # Remove ANSI codes for padding calculation
            import re
            left_plain = re.sub(r'\033\[[0-9;]*m', '', left)
            padding = 38 - len(left_plain)
            print(f"{left}{' ' * padding}  {right}")
        
        print()
        
        # Row 2: Weather + Server
        lines_weather = modules[2].render().split('\n')
        lines_server = modules[3].render().split('\n')
        max_lines = max(len(lines_weather), len(lines_server))
        
        for i in range(max_lines):
            left = lines_weather[i] if i < len(lines_weather) else ' ' * 38
            right = lines_server[i] if i < len(lines_server) else ' ' * 38
            left_plain = re.sub(r'\033\[[0-9;]*m', '', left)
            padding = 38 - len(left_plain)
            print(f"{left}{' ' * padding}  {right}")
        
        print()
        
        # Row 3: Todo + Stats
        lines_todo = modules[4].render().split('\n')
        lines_stats = modules[5].render().split('\n')
        max_lines = max(len(lines_todo), len(lines_stats))
        
        for i in range(max_lines):
            left = lines_todo[i] if i < len(lines_todo) else ' ' * 38
            right = lines_stats[i] if i < len(lines_stats) else ' ' * 38
            left_plain = re.sub(r'\033\[[0-9;]*m', '', left)
            padding = 38 - len(left_plain)
            print(f"{left}{' ' * padding}  {right}")
        
        print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
        print(f"{NeonColors.GREEN}[INFO]{NeonColors.RESET} Press Ctrl+C to exit | Run with --watch for auto-refresh")
        print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")


# ══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN
# ══════════════════════════════════════════════════════════════════════════════

async def run_once():
    """Run dashboard once."""
    config = load_config()
    dashboard = CommandCenter(config)
    await dashboard.fetch_all()
    dashboard.render_dashboard()


async def run_watch(interval: int = 300):
    """Run dashboard in watch mode (auto-refresh)."""
    config = load_config()
    dashboard = CommandCenter(config)
    
    try:
        while True:
            await dashboard.fetch_all()
            dashboard.render_dashboard()
            await asyncio.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n{NeonColors.YELLOW}[EXIT]{NeonColors.RESET} Command Center terminated\n")


if __name__ == "__main__":
    import sys
    
    if "--watch" in sys.argv:
        # Watch mode with auto-refresh
        asyncio.run(run_watch(interval=300))
    else:
        # Single run
        asyncio.run(run_once())

