#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  💼 JOB-HUNTER DEMO - Con datos simulados para demostración                 ║
║  Muestra el flujo completo: scraping → scoring → dedup → export             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import csv
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Set
import time


# ══════════════════════════════════════════════════════════════════════════════
# 🎨 NEON COLORS
# ══════════════════════════════════════════════════════════════════════════════

class NeonColors:
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# ══════════════════════════════════════════════════════════════════════════════
# 📊 DATA STRUCTURES
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class JobListing:
    title: str
    company: str
    location: str
    salary: str
    url: str
    source: str
    keywords_matched: List[str]
    match_score: int
    posted_date: str
    timestamp: str
    job_hash: str


# ══════════════════════════════════════════════════════════════════════════════
# 🎭 SIMULATED DATA
# ══════════════════════════════════════════════════════════════════════════════

SIMULATED_JOBS = [
    # Indeed jobs
    ("Senior Python Engineer", "OpenAI", "Remote", "$180k-$220k", "https://openai.com/careers/senior-python-engineer", "Indeed", "2 days ago"),
    ("AI Engineer", "DeepMind", "London/Remote", "£120k-£160k", "https://deepmind.google/careers/ai-engineer", "Indeed", "1 week ago"),
    ("Machine Learning Engineer", "Anthropic", "San Francisco/Remote", "$170k-$210k", "https://anthropic.com/careers/ml-engineer", "Indeed", "3 days ago"),
    ("Python Developer", "Microsoft", "Redmond, WA", "$140k-$180k", "https://microsoft.com/careers/python-dev", "Indeed", "5 days ago"),
    ("Senior AI Researcher", "Google Brain", "Mountain View, CA", "$200k-$250k", "https://google.com/careers/ai-researcher", "Indeed", "1 day ago"),
    
    # RemoteOK jobs
    ("Remote Python Engineer", "GitLab", "Remote", "$150k-$190k", "https://gitlab.com/careers/python-engineer", "RemoteOK", "4 days ago"),
    ("AI Engineer", "DeepMind", "London/Remote", "£120k-£160k", "https://deepmind.google/careers/ai-engineer", "RemoteOK", "1 week ago"),  # Duplicate
    ("Full Stack Python Developer", "Stripe", "Remote", "$160k-$200k", "https://stripe.com/careers/fullstack-python", "RemoteOK", "2 days ago"),
    ("Machine Learning Engineer", "Hugging Face", "Remote", "$140k-$180k", "https://huggingface.co/careers/ml-engineer", "RemoteOK", "6 days ago"),
    ("Senior Python Backend Engineer", "Notion", "Remote", "$170k-$210k", "https://notion.so/careers/backend-engineer", "RemoteOK", "3 days ago"),
    
    # LinkedIn jobs
    ("Lead AI Engineer", "Tesla", "Palo Alto, CA", "$190k-$240k", "https://tesla.com/careers/lead-ai-engineer", "LinkedIn", "2 days ago"),
    ("Python Machine Learning Engineer", "Netflix", "Los Gatos, CA/Remote", "$180k-$220k", "https://netflix.com/careers/ml-engineer", "LinkedIn", "1 week ago"),
    ("Senior Python Developer", "Amazon", "Seattle, WA", "$160k-$200k", "https://amazon.jobs/python-developer", "LinkedIn", "4 days ago"),
    ("AI Research Engineer", "Meta", "Menlo Park, CA/Remote", "$200k-$250k", "https://meta.com/careers/ai-research", "LinkedIn", "5 days ago"),
    ("Remote Python Engineer", "Shopify", "Remote", "$140k-$180k", "https://shopify.com/careers/python-engineer", "LinkedIn", "3 days ago"),
]

SEARCH_CONFIG = {
    "keywords": ["Python", "AI Engineer", "Remote", "Machine Learning", "Deep Learning"],
}


# ══════════════════════════════════════════════════════════════════════════════
# 🔧 UTILITY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def generate_job_hash(title: str, company: str) -> str:
    """Generate unique hash for job deduplication."""
    combined = f"{title.lower().strip()}|{company.lower().strip()}"
    return hashlib.md5(combined.encode()).hexdigest()[:16]


def calculate_match_score(job: JobListing, config: dict) -> int:
    """Calculate match score (0-100) based on keyword matches."""
    keywords = config["keywords"]
    text_to_search = f"{job.title} {job.location}".lower()
    
    matches = [kw for kw in keywords if kw.lower() in text_to_search]
    
    # Base score
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


def export_to_csv(jobs: List[JobListing], filename: str):
    """Export jobs to CSV file."""
    fieldnames = [
        'title', 'company', 'location', 'salary', 'url',
        'source', 'match_score', 'keywords_matched', 'posted_date'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for job in jobs:
            row = asdict(job)
            row['keywords_matched'] = ', '.join(row['keywords_matched'])
            row.pop('timestamp', None)
            row.pop('job_hash', None)
            writer.writerow(row)
    
    print(f"{NeonColors.GREEN}[SUCCESS]{NeonColors.RESET} Exported to: {NeonColors.BOLD}{filename}{NeonColors.RESET}")


# ══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN DEMO
# ══════════════════════════════════════════════════════════════════════════════

def simulate_scraping():
    """Simulate scraping with realistic delays and logs."""
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.MAGENTA}💼 JOB-HUNTER DEMO - Iniciando búsqueda de empleos...{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
    
    keywords = SEARCH_CONFIG["keywords"]
    print(f"{NeonColors.YELLOW}[CONFIG]{NeonColors.RESET} Keywords: {', '.join(keywords)}")
    print(f"{NeonColors.YELLOW}[CONFIG]{NeonColors.RESET} Location: Remote\n")
    
    all_jobs = []
    sources = {"Indeed": 5, "RemoteOK": 5, "LinkedIn": 5}
    
    # Simulate scraping from each source
    for source, count in sources.items():
        print(f"{NeonColors.CYAN}[FETCH]{NeonColors.RESET} {source}...")
        time.sleep(0.5)  # Simulate network delay
        
        source_jobs = [job for job in SIMULATED_JOBS if job[5] == source]
        
        for job_data in source_jobs:
            title, company, location, salary, url, src, posted = job_data
            
            job_hash = generate_job_hash(title, company)
            text = f"{title} {location}".lower()
            keywords_matched = [kw for kw in keywords if kw.lower() in text]
            
            job = JobListing(
                title=title,
                company=company,
                location=location,
                salary=salary,
                url=url,
                source=src,
                keywords_matched=keywords_matched,
                match_score=0,
                posted_date=posted,
                timestamp=datetime.now().isoformat(),
                job_hash=job_hash
            )
            
            all_jobs.append(job)
            print(f"{NeonColors.MAGENTA}[PARSE]{NeonColors.RESET} {source}: {title[:50]}...")
        
        print(f"{NeonColors.GREEN}[FOUND]{NeonColors.RESET} {source}: {len(source_jobs)} jobs\n")
    
    # Deduplicate
    print(f"{NeonColors.YELLOW}[FILTER]{NeonColors.RESET} Deduplicating jobs...")
    unique_jobs = deduplicate_jobs(all_jobs)
    
    # Calculate match scores
    print(f"{NeonColors.YELLOW}[SCORE]{NeonColors.RESET} Calculating match scores...")
    for job in unique_jobs:
        job.match_score = calculate_match_score(job, SEARCH_CONFIG)
    
    # Sort by score
    unique_jobs.sort(key=lambda j: j.match_score, reverse=True)
    
    # Display high-match jobs
    print(f"\n{NeonColors.CYAN}{'─' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}🎯 HIGH-MATCH JOBS (Score > 80%):{NeonColors.RESET}\n")
    
    high_match_jobs = [j for j in unique_jobs if j.match_score >= 80]
    
    for job in high_match_jobs:
        print(f"{NeonColors.GREEN}[MATCH!]{NeonColors.RESET} {job.title} @ {NeonColors.BOLD}{job.company}{NeonColors.RESET} ({job.match_score}% match)")
        print(f"  📍 Location: {job.location}")
        print(f"  💰 Salary: {job.salary}")
        print(f"  🏷️  Keywords: {', '.join(job.keywords_matched)}")
        print(f"  📅 Posted: {job.posted_date}")
        print(f"  🔗 URL: {job.url[:60]}...")
        print()
    
    # Export to CSV
    timestamp = datetime.now().strftime("%Y-%m-%d")
    output_file = f"output/job_listings_{timestamp}.csv"
    export_to_csv(unique_jobs, output_file)
    
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.YELLOW}[STATS]{NeonColors.RESET} Total jobs found: {NeonColors.BOLD}{len(all_jobs)}{NeonColors.RESET}")
    print(f"{NeonColors.YELLOW}[STATS]{NeonColors.RESET} After deduplication: {NeonColors.BOLD}{len(unique_jobs)}{NeonColors.RESET}")
    print(f"{NeonColors.YELLOW}[STATS]{NeonColors.RESET} High-match jobs (>80%): {NeonColors.BOLD}{len(high_match_jobs)}{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")


if __name__ == "__main__":
    try:
        simulate_scraping()
    except KeyboardInterrupt:
        print(f"\n{NeonColors.YELLOW}[ABORT]{NeonColors.RESET} Job hunting interrupted")
    except Exception as e:
        print(f"\n{NeonColors.RED}[FATAL]{NeonColors.RESET} {e}")

