#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🐕 WATCHDOG - Intelligence Pipeline Monitor                                ║
║  Automated pipeline: Scrape → Analyze → Alert                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import json
import subprocess
import time
import os
from datetime import datetime
from typing import List, Dict, Set
import platform


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

CONFIG = {
    # Keywords to watch for (case-insensitive)
    "watch_keywords": [
        "ai", "artificial intelligence", "gpt", "llm",
        "rust", "python", "javascript",
        "crypto", "bitcoin", "ethereum",
        "security", "vulnerability", "breach",
        "startup", "funding", "ipo",
    ],
    
    # Alert threshold (minimum mentions to trigger alert)
    "alert_threshold": 2,
    
    # Scan interval (seconds)
    "scan_interval": 300,  # 5 minutes
    
    # Enable sound alerts
    "sound_alerts": True,
    
    # Enable desktop notifications (Windows)
    "desktop_notifications": True,
}


# ══════════════════════════════════════════════════════════════════════════════
# 🔊 ALERT SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

def play_alert_sound():
    """Play system beep (cross-platform)."""
    if CONFIG["sound_alerts"]:
        try:
            if platform.system() == "Windows":
                import winsound
                # Play a beep: frequency 1000Hz, duration 500ms
                winsound.Beep(1000, 500)
            else:
                # Unix/Linux: use system bell
                print('\a')
        except Exception as e:
            print(f"{NeonColors.YELLOW}[WARN]{NeonColors.RESET} Could not play sound: {e}")


def show_desktop_notification(title: str, message: str):
    """Show desktop notification (Windows only)."""
    if not CONFIG["desktop_notifications"]:
        return
    
    try:
        if platform.system() == "Windows":
            # PowerShell balloon notification
            ps_script = f'''
            Add-Type -AssemblyName System.Windows.Forms
            $notification = New-Object System.Windows.Forms.NotifyIcon
            $notification.Icon = [System.Drawing.SystemIcons]::Information
            $notification.BalloonTipTitle = "{title}"
            $notification.BalloonTipText = "{message}"
            $notification.Visible = $True
            $notification.ShowBalloonTip(5000)
            Start-Sleep -Seconds 2
            $notification.Dispose()
            '''
            subprocess.run(["powershell", "-Command", ps_script], 
                         capture_output=True, timeout=10)
    except Exception as e:
        print(f"{NeonColors.YELLOW}[WARN]{NeonColors.RESET} Could not show notification: {e}")


def alert(keyword: str, count: int, articles: List[str]):
    """Trigger alert for detected keyword."""
    print(f"\n{NeonColors.RED}{'!' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.RED}🚨 ALERT: '{keyword}' DETECTED! 🚨{NeonColors.RESET}")
    print(f"{NeonColors.RED}{'!' * 78}{NeonColors.RESET}\n")
    
    print(f"{NeonColors.YELLOW}[ALERT]{NeonColors.RESET} Found {NeonColors.BOLD}{count}{NeonColors.RESET} mentions")
    print(f"{NeonColors.YELLOW}[ALERT]{NeonColors.RESET} Related articles:\n")
    
    for i, article in enumerate(articles[:3], 1):
        print(f"  {NeonColors.CYAN}{i}.{NeonColors.RESET} {article}")
    
    print()
    
    # Play sound
    play_alert_sound()
    
    # Desktop notification
    show_desktop_notification(
        f"🚨 Watchdog Alert: {keyword}",
        f"Found {count} mentions in latest scan"
    )


# ══════════════════════════════════════════════════════════════════════════════
# 🔍 MONITORING
# ══════════════════════════════════════════════════════════════════════════════

def run_harvester() -> bool:
    """Run Info-Harvester to collect fresh data."""
    try:
        print(f"{NeonColors.CYAN}[HARVEST]{NeonColors.RESET} Running Info-Harvester...")
        result = subprocess.run(
            ["python", "output/info_harvester.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"{NeonColors.GREEN}[SUCCESS]{NeonColors.RESET} Data harvested")
            return True
        else:
            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Harvester failed")
            return False
    except Exception as e:
        print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Harvester error: {e}")
        return False


def run_analyst() -> bool:
    """Run Analyst to analyze data."""
    try:
        print(f"{NeonColors.CYAN}[ANALYZE]{NeonColors.RESET} Running Analyst...")
        result = subprocess.run(
            ["python", "output/analyst.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"{NeonColors.GREEN}[SUCCESS]{NeonColors.RESET} Analysis complete")
            return True
        else:
            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Analyst failed")
            return False
    except Exception as e:
        print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Analyst error: {e}")
        return False


def check_for_keywords() -> Dict[str, List[str]]:
    """
    Check intelligence report for watched keywords.
    Returns dict of {keyword: [matching_articles]}
    """
    matches = {}
    
    try:
        with open('output/intelligence_report.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        articles = data.get('articles', [])
        watch_keywords = [kw.lower() for kw in CONFIG['watch_keywords']]
        
        for keyword in watch_keywords:
            matching_articles = []
            
            for article in articles:
                title = article.get('title', '').lower()
                
                if keyword in title:
                    matching_articles.append(article.get('title', 'Unknown'))
            
            if len(matching_articles) >= CONFIG['alert_threshold']:
                matches[keyword] = matching_articles
        
        return matches
        
    except Exception as e:
        print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Could not check keywords: {e}")
        return {}


# ══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN WATCHDOG LOOP
# ══════════════════════════════════════════════════════════════════════════════

def watchdog_loop():
    """Main monitoring loop."""
    scan_count = 0
    
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.MAGENTA}🐕 WATCHDOG - Intelligence Pipeline Monitor{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
    
    print(f"{NeonColors.YELLOW}[CONFIG]{NeonColors.RESET} Watching for: {', '.join(CONFIG['watch_keywords'][:5])}...")
    print(f"{NeonColors.YELLOW}[CONFIG]{NeonColors.RESET} Alert threshold: {CONFIG['alert_threshold']} mentions")
    print(f"{NeonColors.YELLOW}[CONFIG]{NeonColors.RESET} Scan interval: {CONFIG['scan_interval']}s ({CONFIG['scan_interval']//60} min)")
    print(f"{NeonColors.YELLOW}[CONFIG]{NeonColors.RESET} Sound alerts: {CONFIG['sound_alerts']}")
    print(f"{NeonColors.YELLOW}[CONFIG]{NeonColors.RESET} Desktop notifications: {CONFIG['desktop_notifications']}\n")
    
    print(f"{NeonColors.GREEN}[START]{NeonColors.RESET} Watchdog monitoring started")
    print(f"{NeonColors.GREEN}[INFO]{NeonColors.RESET} Press Ctrl+C to stop\n")
    
    try:
        while True:
            scan_count += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"{NeonColors.CYAN}{'─' * 78}{NeonColors.RESET}")
            print(f"{NeonColors.BOLD}[SCAN #{scan_count}]{NeonColors.RESET} {timestamp}")
            print(f"{NeonColors.CYAN}{'─' * 78}{NeonColors.RESET}\n")
            
            # Step 1: Harvest data
            if not run_harvester():
                print(f"{NeonColors.YELLOW}[SKIP]{NeonColors.RESET} Skipping analysis due to harvest failure\n")
                time.sleep(CONFIG['scan_interval'])
                continue
            
            # Step 2: Analyze data
            if not run_analyst():
                print(f"{NeonColors.YELLOW}[SKIP]{NeonColors.RESET} Skipping keyword check due to analysis failure\n")
                time.sleep(CONFIG['scan_interval'])
                continue
            
            # Step 3: Check for keywords
            matches = check_for_keywords()
            
            if matches:
                print(f"\n{NeonColors.GREEN}[FOUND]{NeonColors.RESET} Detected {len(matches)} keyword(s)!\n")
                
                for keyword, articles in matches.items():
                    alert(keyword, len(articles), articles)
            else:
                print(f"{NeonColors.BLUE}[INFO]{NeonColors.RESET} No alerts triggered")
            
            # Wait for next scan
            print(f"\n{NeonColors.CYAN}[SLEEP]{NeonColors.RESET} Next scan in {CONFIG['scan_interval']}s...\n")
            time.sleep(CONFIG['scan_interval'])
            
    except KeyboardInterrupt:
        print(f"\n\n{NeonColors.YELLOW}[STOP]{NeonColors.RESET} Watchdog monitoring stopped by user")
        print(f"{NeonColors.GREEN}[STATS]{NeonColors.RESET} Total scans completed: {scan_count}\n")


def run_single_scan():
    """Run a single scan (for testing)."""
    print(f"{NeonColors.CYAN}[MODE]{NeonColors.RESET} Single scan mode\n")
    
    if run_harvester() and run_analyst():
        matches = check_for_keywords()
        
        if matches:
            for keyword, articles in matches.items():
                alert(keyword, len(articles), articles)
        else:
            print(f"{NeonColors.BLUE}[INFO]{NeonColors.RESET} No keywords detected above threshold\n")


# ══════════════════════════════════════════════════════════════════════════════
# 🎯 ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        # Single scan mode
        run_single_scan()
    else:
        # Continuous monitoring mode
        watchdog_loop()

