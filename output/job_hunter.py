#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  💼 JOB-HUNTER - Buscador de Empleos Automatizado                           ║
║  Multi-board job scraper with keyword matching and scoring                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import csv
import hashlib
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional, Set
from urllib.parse import urljoin, quote

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
class JobListing:
    """Unified data structure for job listings."""
    title: str
    company: str
    location: str
    salary: Optional[str]
    url: str
    source: str
    keywords_matched: List[str]
    match_score: int
    posted_date: str
    timestamp: str
    job_hash: str  # For deduplication
    
    def to_dict(self):
        return asdict(self)


# ══════════════════════════════════════════════════════════════════════════════
# ⚙️ CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

SEARCH_CONFIG = {
    "keywords": ["Python", "AI Engineer", "Remote", "Machine Learning", "Deep Learning"],
    "location": "Remote",
    "min_salary": 100000,  # Minimum salary in USD
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


# ══════════════════════════════════════════════════════════════════════════════
# 🔧 UTILITY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def generate_job_hash(title: str, company: str) -> str:
    """Generate unique hash for job deduplication."""
    combined = f"{title.lower().strip()}|{company.lower().strip()}"
    return hashlib.md5(combined.encode()).hexdigest()[:16]


def parse_salary(text: str) -> Optional[str]:
    """
    Parse salary from various formats.
    Examples: "$100k-$150k", "100000-150000", "£80k", "€90,000"
    """
    if not text:
        return None
    
    # Pattern for salary ranges
    patterns = [
        r'\$?\d{1,3}[,\.]?\d{0,3}k?\s*-\s*\$?\d{1,3}[,\.]?\d{0,3}k?',  # $100k-$150k
        r'\d{3,6}[,\.]?\d{0,3}\s*-\s*\d{3,6}[,\.]?\d{0,3}',  # 100000-150000
        r'\$\d{1,3}[,\.]?\d{0,3}k?',  # $100k
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return None


def calculate_match_score(job: JobListing, config: dict) -> int:
    """
    Calculate match score (0-100) based on keyword matches.
    More keywords matched = higher score.
    """
    keywords = config["keywords"]
    text_to_search = f"{job.title} {job.location}".lower()
    
    matches = [kw for kw in keywords if kw.lower() in text_to_search]
    
    # Base score: percentage of keywords matched
    base_score = int((len(matches) / len(keywords)) * 70)
    
    # Bonus points
    bonus = 0
    if "remote" in text_to_search:
        bonus += 15
    if "senior" in text_to_search or "lead" in text_to_search:
        bonus += 10
    if job.salary:
        bonus += 5
    
    return min(base_score + bonus, 100)


# ══════════════════════════════════════════════════════════════════════════════
# 🕷️ SCRAPERS
# ══════════════════════════════════════════════════════════════════════════════

async def scrape_indeed(
    session: aiohttp.ClientSession,
    keywords: List[str],
    location: str,
    semaphore: asyncio.Semaphore
) -> List[JobListing]:
    """Scrape Indeed job listings."""
    jobs = []
    query = " ".join(keywords)
    url = f"https://www.indeed.com/jobs?q={quote(query)}&l={quote(location)}"
    
    async with semaphore:
        try:
            headers = {"User-Agent": USER_AGENTS[0]}
            print(f"{NeonColors.CYAN}[FETCH]{NeonColors.RESET} Indeed: {query}")
            
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status != 200:
                    print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Indeed returned {response.status}")
                    return jobs
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Parse Indeed job cards
                job_cards = soup.select('.job_seen_beacon, .jobsearch-SerpJobCard')[:15]
                
                for card in job_cards:
                    try:
                        title_elem = card.select_one('h2.jobTitle a, .jobTitle span')
                        company_elem = card.select_one('.companyName')
                        location_elem = card.select_one('.companyLocation')
                        salary_elem = card.select_one('.salary-snippet')
                        
                        if not title_elem or not company_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        company = company_elem.get_text(strip=True)
                        job_location = location_elem.get_text(strip=True) if location_elem else "Not specified"
                        salary = parse_salary(salary_elem.get_text()) if salary_elem else None
                        
                        # Get job URL
                        link_elem = card.select_one('a[data-jk]')
                        job_url = urljoin(url, link_elem['href']) if link_elem else url
                        
                        job_hash = generate_job_hash(title, company)
                        keywords_matched = [kw for kw in keywords if kw.lower() in title.lower()]
                        
                        job = JobListing(
                            title=title,
                            company=company,
                            location=job_location,
                            salary=salary,
                            url=job_url,
                            source="Indeed",
                            keywords_matched=keywords_matched,
                            match_score=0,  # Will be calculated later
                            posted_date="Recently",
                            timestamp=datetime.now().isoformat(),
                            job_hash=job_hash
                        )
                        
                        jobs.append(job)
                        
                    except Exception as e:
                        print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Parsing Indeed job: {e}")
                        continue
                
                print(f"{NeonColors.GREEN}[FOUND]{NeonColors.RESET} Indeed: {len(jobs)} jobs")
                
        except asyncio.TimeoutError:
            print(f"{NeonColors.RED}[TIMEOUT]{NeonColors.RESET} Indeed")
        except Exception as e:
            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Scraping Indeed: {e}")
    
    return jobs


async def scrape_remoteok(
    session: aiohttp.ClientSession,
    keywords: List[str],
    semaphore: asyncio.Semaphore
) -> List[JobListing]:
    """Scrape RemoteOK job listings."""
    jobs = []
    query = "-".join([kw.lower().replace(" ", "-") for kw in keywords[:2]])
    url = f"https://remoteok.com/remote-{query}-jobs"
    
    async with semaphore:
        try:
            headers = {"User-Agent": USER_AGENTS[1]}
            print(f"{NeonColors.CYAN}[FETCH]{NeonColors.RESET} RemoteOK: {query}")
            
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status != 200:
                    print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} RemoteOK returned {response.status}")
                    return jobs
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Parse RemoteOK job rows
                job_rows = soup.select('tr.job')[:15]
                
                for row in job_rows:
                    try:
                        title_elem = row.select_one('h2.title')
                        company_elem = row.select_one('h3.company')
                        salary_elem = row.select_one('.salary')
                        link_elem = row.select_one('a.preventLink')
                        
                        if not title_elem or not company_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        company = company_elem.get_text(strip=True)
                        salary = parse_salary(salary_elem.get_text()) if salary_elem else None
                        job_url = urljoin(url, link_elem['href']) if link_elem else url
                        
                        job_hash = generate_job_hash(title, company)
                        keywords_matched = [kw for kw in keywords if kw.lower() in title.lower()]
                        
                        job = JobListing(
                            title=title,
                            company=company,
                            location="Remote",
                            salary=salary,
                            url=job_url,
                            source="RemoteOK",
                            keywords_matched=keywords_matched,
                            match_score=0,
                            posted_date="Recently",
                            timestamp=datetime.now().isoformat(),
                            job_hash=job_hash
                        )
                        
                        jobs.append(job)
                        
                    except Exception as e:
                        print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Parsing RemoteOK job: {e}")
                        continue
                
                print(f"{NeonColors.GREEN}[FOUND]{NeonColors.RESET} RemoteOK: {len(jobs)} jobs")
                
        except asyncio.TimeoutError:
            print(f"{NeonColors.RED}[TIMEOUT]{NeonColors.RESET} RemoteOK")
        except Exception as e:
            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Scraping RemoteOK: {e}")
    
    return jobs


# ══════════════════════════════════════════════════════════════════════════════
# 🔄 DEDUPLICATION & FILTERING
# ══════════════════════════════════════════════════════════════════════════════

def deduplicate_jobs(jobs: List[JobListing]) -> List[JobListing]:
    """Remove duplicate jobs based on hash."""
    seen_hashes: Set[str] = set()
    unique_jobs = []
    
    for job in jobs:
        if job.job_hash not in seen_hashes:
            seen_hashes.add(job.job_hash)
            unique_jobs.append(job)
    
    duplicates_removed = len(jobs) - len(unique_jobs)
    if duplicates_removed > 0:
        print(f"{NeonColors.YELLOW}[FILTER]{NeonColors.RESET} Removed {duplicates_removed} duplicates")
    
    return unique_jobs


# ══════════════════════════════════════════════════════════════════════════════
# 💾 EXPORT
# ══════════════════════════════════════════════════════════════════════════════

def export_to_csv(jobs: List[JobListing], filename: str):
    """Export jobs to CSV file."""
    if not jobs:
        print(f"{NeonColors.YELLOW}[WARN]{NeonColors.RESET} No jobs to export")
        return
    
    fieldnames = [
        'title', 'company', 'location', 'salary', 'url',
        'source', 'match_score', 'keywords_matched', 'posted_date'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for job in jobs:
            row = job.to_dict()
            row['keywords_matched'] = ', '.join(row['keywords_matched'])
            # Remove fields not in CSV
            row.pop('timestamp', None)
            row.pop('job_hash', None)
            writer.writerow(row)
    
    print(f"{NeonColors.GREEN}[SUCCESS]{NeonColors.RESET} Exported to: {NeonColors.BOLD}{filename}{NeonColors.RESET}")


# ══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════════════════

async def hunt_jobs():
    """Main job hunting orchestrator."""
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.MAGENTA}💼 JOB-HUNTER - Iniciando búsqueda de empleos...{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
    
    keywords = SEARCH_CONFIG["keywords"]
    location = SEARCH_CONFIG["location"]
    
    print(f"{NeonColors.YELLOW}[CONFIG]{NeonColors.RESET} Keywords: {', '.join(keywords)}")
    print(f"{NeonColors.YELLOW}[CONFIG]{NeonColors.RESET} Location: {location}\n")
    
    # Semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(3)
    
    # Create aiohttp session
    connector = aiohttp.TCPConnector(limit=10)
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        # Scrape all sources concurrently
        tasks = [
            scrape_indeed(session, keywords, location, semaphore),
            scrape_remoteok(session, keywords, semaphore),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine results
        all_jobs = []
        for result in results:
            if isinstance(result, list):
                all_jobs.extend(result)
            elif isinstance(result, Exception):
                print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Task failed: {result}")
        
        # Deduplicate
        unique_jobs = deduplicate_jobs(all_jobs)
        
        # Calculate match scores
        for job in unique_jobs:
            job.match_score = calculate_match_score(job, SEARCH_CONFIG)
        
        # Sort by match score (highest first)
        unique_jobs.sort(key=lambda j: j.match_score, reverse=True)
        
        # Display high-match jobs
        print(f"\n{NeonColors.CYAN}{'─' * 78}{NeonColors.RESET}")
        print(f"{NeonColors.BOLD}🎯 HIGH-MATCH JOBS (Score > 80%):{NeonColors.RESET}\n")
        
        high_match_jobs = [j for j in unique_jobs if j.match_score >= 80]
        
        for job in high_match_jobs:
            print(f"{NeonColors.GREEN}[MATCH!]{NeonColors.RESET} {job.title} @ {NeonColors.BOLD}{job.company}{NeonColors.RESET} ({job.match_score}% match)")
            print(f"  📍 Location: {job.location}")
            if job.salary:
                print(f"  💰 Salary: {job.salary}")
            print(f"  🔗 URL: {job.url}")
            print(f"  🏷️  Keywords: {', '.join(job.keywords_matched)}")
            print()
        
        # Export to CSV
        timestamp = datetime.now().strftime("%Y-%m-%d")
        output_file = f"output/job_listings_{timestamp}.csv"
        export_to_csv(unique_jobs, output_file)
        
        print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
        print(f"{NeonColors.YELLOW}[STATS]{NeonColors.RESET} Total jobs found: {NeonColors.BOLD}{len(unique_jobs)}{NeonColors.RESET}")
        print(f"{NeonColors.YELLOW}[STATS]{NeonColors.RESET} High-match jobs: {NeonColors.BOLD}{len(high_match_jobs)}{NeonColors.RESET}")
        print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")


# ══════════════════════════════════════════════════════════════════════════════
# 🎯 ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        asyncio.run(hunt_jobs())
    except KeyboardInterrupt:
        print(f"\n{NeonColors.YELLOW}[ABORT]{NeonColors.RESET} Job hunting interrupted by user")
    except Exception as e:
        print(f"\n{NeonColors.RED}[FATAL]{NeonColors.RESET} {e}")

