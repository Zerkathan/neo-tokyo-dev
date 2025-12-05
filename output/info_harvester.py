#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔮 INFO-HARVESTER - Agregador de Noticias Cyberpunk                        ║
║  Scraper asíncrono de alto rendimiento para Hacker News + TechCrunch        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import json
import random
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup


# ══════════════════════════════════════════════════════════════════════════════
# 🎨 NEON COLORS
# ══════════════════════════════════════════════════════════════════════════════

class NeonColors:
    """ANSI color codes for cyberpunk-style terminal output."""
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
class Article:
    """Unified data structure for news articles."""
    title: str
    url: str
    score: Optional[int]
    source: str
    timestamp: str
    
    def to_dict(self):
        return asdict(self)


# ══════════════════════════════════════════════════════════════════════════════
# 🤖 USER AGENT ROTATION
# ══════════════════════════════════════════════════════════════════════════════

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
]


# ══════════════════════════════════════════════════════════════════════════════
# 🕷️ SCRAPERS
# ══════════════════════════════════════════════════════════════════════════════

async def fetch_hacker_news(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore) -> List[Article]:
    """Fetch and parse Hacker News front page."""
    url = "https://news.ycombinator.com/"
    articles = []
    
    async with semaphore:
        try:
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            print(f"{NeonColors.CYAN}[FETCH]{NeonColors.RESET} Requesting {NeonColors.BOLD}{url}{NeonColors.RESET}")
            
            async with session.get(url, headers=headers, timeout=10) as response:
                status = response.status
                
                if status == 200:
                    print(f"{NeonColors.GREEN}[✓ OK]{NeonColors.RESET} {status} - {url}")
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Parse HN structure
                    items = soup.select('.athing')[:10]  # Top 10 stories
                    
                    for item in items:
                        try:
                            title_elem = item.select_one('.titleline > a')
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            link = title_elem.get('href', '')
                            
                            # Get score from next sibling
                            score_elem = item.find_next_sibling('tr')
                            score = 0
                            if score_elem:
                                score_span = score_elem.select_one('.score')
                                if score_span:
                                    score_text = score_span.get_text()
                                    score = int(score_text.split()[0])
                            
                            # Normalize URL
                            if not link.startswith('http'):
                                link = urljoin(url, link)
                            
                            article = Article(
                                title=title,
                                url=link,
                                score=score,
                                source="Hacker News",
                                timestamp=datetime.now().isoformat()
                            )
                            articles.append(article)
                            
                            print(f"{NeonColors.MAGENTA}[PARSE]{NeonColors.RESET} HN: {title[:60]}... ({score} pts)")
                            
                        except Exception as e:
                            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Parsing HN item: {e}")
                            continue
                    
                    print(f"{NeonColors.GREEN}[DONE]{NeonColors.RESET} Hacker News: {len(articles)} articles extracted")
                    
                else:
                    print(f"{NeonColors.RED}[✗ FAIL]{NeonColors.RESET} {status} - {url}")
                    
        except asyncio.TimeoutError:
            print(f"{NeonColors.RED}[TIMEOUT]{NeonColors.RESET} {url}")
        except Exception as e:
            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Fetching HN: {e}")
    
    return articles


async def fetch_techcrunch(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore) -> List[Article]:
    """Fetch and parse TechCrunch front page."""
    url = "https://techcrunch.com/"
    articles = []
    
    async with semaphore:
        try:
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            print(f"{NeonColors.CYAN}[FETCH]{NeonColors.RESET} Requesting {NeonColors.BOLD}{url}{NeonColors.RESET}")
            
            async with session.get(url, headers=headers, timeout=10) as response:
                status = response.status
                
                if status == 200:
                    print(f"{NeonColors.GREEN}[✓ OK]{NeonColors.RESET} {status} - {url}")
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Parse TechCrunch structure (multiple possible selectors)
                    # Try different article containers
                    article_elems = (
                        soup.select('article.post-block')[:10] or
                        soup.select('.post-block')[:10] or
                        soup.select('article')[:10]
                    )
                    
                    for elem in article_elems:
                        try:
                            # Try to find title
                            title_elem = (
                                elem.select_one('h2 a') or
                                elem.select_one('h3 a') or
                                elem.select_one('.post-block__title a') or
                                elem.select_one('a')
                            )
                            
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            link = title_elem.get('href', '')
                            
                            # Normalize URL
                            if not link.startswith('http'):
                                link = urljoin(url, link)
                            
                            article = Article(
                                title=title,
                                url=link,
                                score=None,  # TechCrunch doesn't have scores
                                source="TechCrunch",
                                timestamp=datetime.now().isoformat()
                            )
                            articles.append(article)
                            
                            print(f"{NeonColors.MAGENTA}[PARSE]{NeonColors.RESET} TC: {title[:60]}...")
                            
                        except Exception as e:
                            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Parsing TC item: {e}")
                            continue
                    
                    print(f"{NeonColors.GREEN}[DONE]{NeonColors.RESET} TechCrunch: {len(articles)} articles extracted")
                    
                else:
                    print(f"{NeonColors.RED}[✗ FAIL]{NeonColors.RESET} {status} - {url}")
                    
        except asyncio.TimeoutError:
            print(f"{NeonColors.RED}[TIMEOUT]{NeonColors.RESET} {url}")
        except Exception as e:
            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Fetching TC: {e}")
    
    return articles


# ══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════════════════

async def harvest_intelligence():
    """Main async orchestrator for Info-Harvester."""
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.MAGENTA}🔮 INFO-HARVESTER - Iniciando recolección de inteligencia...{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
    
    # Semaphore to limit concurrent requests (max 5)
    semaphore = asyncio.Semaphore(5)
    
    # Create aiohttp session
    connector = aiohttp.TCPConnector(limit=10)
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        # Fetch from both sources concurrently
        tasks = [
            fetch_hacker_news(session, semaphore),
            fetch_techcrunch(session, semaphore),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine results
        all_articles = []
        for result in results:
            if isinstance(result, list):
                all_articles.extend(result)
            elif isinstance(result, Exception):
                print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Task failed: {result}")
        
        # Prepare output structure
        output = {
            "metadata": {
                "harvested_at": datetime.now().isoformat(),
                "total_articles": len(all_articles),
                "sources": ["Hacker News", "TechCrunch"]
            },
            "articles": [article.to_dict() for article in all_articles]
        }
        
        # Save to JSON
        output_file = "output/intelligence_report.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
        print(f"{NeonColors.GREEN}[SUCCESS]{NeonColors.RESET} Intelligence report saved to: {NeonColors.BOLD}{output_file}{NeonColors.RESET}")
        print(f"{NeonColors.YELLOW}[STATS]{NeonColors.RESET} Total articles: {NeonColors.BOLD}{len(all_articles)}{NeonColors.RESET}")
        print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")


# ══════════════════════════════════════════════════════════════════════════════
# 🎯 ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        asyncio.run(harvest_intelligence())
    except KeyboardInterrupt:
        print(f"\n{NeonColors.YELLOW}[ABORT]{NeonColors.RESET} Harvesting interrupted by user")
    except Exception as e:
        print(f"\n{NeonColors.RED}[FATAL]{NeonColors.RESET} {e}")

