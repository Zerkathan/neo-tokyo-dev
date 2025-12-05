#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🧠 ANALYST - Intelligence Data Analyzer                                    ║
║  Analyzes intelligence_report.json to extract trending topics               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import json
import re
from collections import Counter
from datetime import datetime
from typing import List, Dict, Tuple


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
# 📋 STOPWORDS (English common words to exclude)
# ══════════════════════════════════════════════════════════════════════════════

STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
    'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will',
    'with', 'the', 'this', 'but', 'they', 'have', 'had', 'what', 'when', 'where',
    'who', 'which', 'why', 'how', 'or', 'than', 'so', 'if', 'then', 'can', 'could',
    'may', 'might', 'must', 'should', 'would', 'been', 'being', 'i', 'you', 'we',
    'my', 'your', 'their', 'his', 'her', 'one', 'two', 'all', 'some', 'any',
    'more', 'most', 'now', 'new', 'just', 'also', 'get', 'make', 'after', 'into',
    'about', 'over', 'only', 'other', 'there', 'out', 'up', 'down', 'through',
}


# ══════════════════════════════════════════════════════════════════════════════
# 🔧 DATA PROCESSING
# ══════════════════════════════════════════════════════════════════════════════

def read_intelligence_report(filepath: str) -> Dict:
    """Read intelligence report JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"{NeonColors.GREEN}[SUCCESS]{NeonColors.RESET} Loaded: {filepath}")
        return data
    except FileNotFoundError:
        print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} File not found: {filepath}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Invalid JSON: {e}")
        exit(1)


def extract_keywords(text: str) -> List[str]:
    """
    Extract keywords from text.
    - Convert to lowercase
    - Remove special characters
    - Filter stopwords
    - Return words with 3+ characters
    """
    # Convert to lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^\w\s-]', ' ', text)
    
    # Split into words
    words = text.split()
    
    # Filter: remove stopwords, keep only words with 3+ chars
    keywords = [
        word for word in words
        if word not in STOPWORDS and len(word) >= 3
    ]
    
    return keywords


def analyze_trending_topics(articles: List[Dict], top_n: int = 10) -> Counter:
    """
    Analyze articles to find trending topics.
    Returns Counter with word frequencies.
    """
    all_keywords = []
    
    for article in articles:
        title = article.get('title', '')
        keywords = extract_keywords(title)
        all_keywords.extend(keywords)
    
    return Counter(all_keywords)


def identify_clusters(word_freq: Counter) -> Dict[str, List[str]]:
    """
    Identify thematic clusters based on common tech topics.
    """
    clusters = {
        "🤖 AI & Machine Learning": [],
        "💻 Programming & Dev": [],
        "🔐 Security & Privacy": [],
        "🌐 Web & Cloud": [],
        "⚡ Performance & Optimization": [],
        "📱 Mobile & Hardware": [],
        "💰 Business & Startups": [],
        "🎮 Gaming & Graphics": [],
        "📊 Data & Analytics": [],
        "🔧 Tools & Infrastructure": [],
    }
    
    # Keywords for each cluster
    cluster_keywords = {
        "🤖 AI & Machine Learning": ['ai', 'machine', 'learning', 'neural', 'model', 'llm', 'gpt', 'transformer', 'deep'],
        "💻 Programming & Dev": ['code', 'programming', 'python', 'javascript', 'rust', 'go', 'developer', 'coding'],
        "🔐 Security & Privacy": ['security', 'privacy', 'encryption', 'hack', 'vulnerability', 'breach', 'crypto'],
        "🌐 Web & Cloud": ['web', 'cloud', 'aws', 'server', 'api', 'http', 'browser'],
        "⚡ Performance & Optimization": ['performance', 'optimization', 'speed', 'fast', 'benchmark', 'efficient'],
        "📱 Mobile & Hardware": ['mobile', 'phone', 'hardware', 'chip', 'processor', 'device'],
        "💰 Business & Startups": ['startup', 'business', 'market', 'company', 'ceo', 'funding'],
        "🎮 Gaming & Graphics": ['game', 'gaming', 'graphics', 'gpu', 'render', 'engine'],
        "📊 Data & Analytics": ['data', 'analytics', 'database', 'sql', 'storage'],
        "🔧 Tools & Infrastructure": ['tool', 'framework', 'library', 'infrastructure', 'docker', 'kubernetes'],
    }
    
    # Assign words to clusters
    for word, freq in word_freq.items():
        for cluster_name, keywords in cluster_keywords.items():
            if word in keywords:
                clusters[cluster_name].append((word, freq))
                break
    
    # Remove empty clusters
    clusters = {k: v for k, v in clusters.items() if v}
    
    return clusters


# ══════════════════════════════════════════════════════════════════════════════
# 📊 REPORTING
# ══════════════════════════════════════════════════════════════════════════════

def print_trending_topics(word_freq: Counter, top_n: int = 10):
    """Print trending topics to terminal with neon styling."""
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.MAGENTA}📊 TOP {top_n} TRENDING TOPICS{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
    
    for i, (word, freq) in enumerate(word_freq.most_common(top_n), 1):
        bar = '█' * min(freq * 2, 40)  # Visual bar
        print(f"{NeonColors.YELLOW}[{i:2d}]{NeonColors.RESET} {NeonColors.GREEN}{word:20s}{NeonColors.RESET} {NeonColors.CYAN}{bar}{NeonColors.RESET} {NeonColors.BOLD}{freq}{NeonColors.RESET}")


def print_clusters(clusters: Dict[str, List[Tuple[str, int]]]):
    """Print thematic clusters."""
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.MAGENTA}🎯 THEMATIC CLUSTERS{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
    
    for cluster_name, words in sorted(clusters.items(), key=lambda x: sum(w[1] for w in x[1]), reverse=True):
        if not words:
            continue
        
        total_freq = sum(w[1] for w in words)
        print(f"{NeonColors.BOLD}{cluster_name}{NeonColors.RESET} ({NeonColors.YELLOW}{total_freq}{NeonColors.RESET} mentions)")
        
        # Top 3 words in this cluster
        top_words = sorted(words, key=lambda x: x[1], reverse=True)[:3]
        for word, freq in top_words:
            print(f"  {NeonColors.GREEN}•{NeonColors.RESET} {word} ({freq})")
        print()


def export_to_markdown(data: Dict, word_freq: Counter, clusters: Dict, filepath: str):
    """Export intelligence summary to Markdown."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("# 🧠 Intelligence Summary Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Metadata
        metadata = data.get('metadata', {})
        f.write("## 📊 Dataset Info\n\n")
        f.write(f"- **Total Articles:** {metadata.get('total_articles', 'N/A')}\n")
        f.write(f"- **Sources:** {', '.join(metadata.get('sources', []))}\n")
        f.write(f"- **Harvested:** {metadata.get('harvested_at', 'N/A')}\n\n")
        
        # Top topics
        f.write("## 🔥 Top 10 Trending Topics\n\n")
        for i, (word, freq) in enumerate(word_freq.most_common(10), 1):
            bar = '▓' * min(freq * 2, 30)
            f.write(f"{i}. **{word}** `{bar}` ({freq} mentions)\n")
        f.write("\n")
        
        # Thematic clusters
        f.write("## 🎯 Thematic Analysis\n\n")
        for cluster_name, words in sorted(clusters.items(), key=lambda x: sum(w[1] for w in x[1]), reverse=True):
            if not words:
                continue
            
            total_freq = sum(w[1] for w in words)
            f.write(f"### {cluster_name} ({total_freq} mentions)\n\n")
            
            top_words = sorted(words, key=lambda x: x[1], reverse=True)
            for word, freq in top_words:
                f.write(f"- **{word}**: {freq} mentions\n")
            f.write("\n")
        
        # Top articles
        f.write("## 📰 Most Relevant Articles\n\n")
        articles = data.get('articles', [])
        for i, article in enumerate(articles[:5], 1):
            f.write(f"{i}. **{article.get('title', 'N/A')}**\n")
            f.write(f"   - Source: {article.get('source', 'N/A')}\n")
            if article.get('score'):
                f.write(f"   - Score: {article.get('score')} points\n")
            f.write(f"   - [Read more]({article.get('url', '#')})\n\n")
    
    print(f"{NeonColors.GREEN}[SUCCESS]{NeonColors.RESET} Markdown report exported: {NeonColors.BOLD}{filepath}{NeonColors.RESET}")


# ══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Main analysis pipeline."""
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.MAGENTA}🧠 ANALYST - Intelligence Data Analyzer{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
    
    # Read data
    data = read_intelligence_report('output/intelligence_report.json')
    
    articles = data.get('articles', [])
    total_articles = len(articles)
    
    print(f"{NeonColors.YELLOW}[INFO]{NeonColors.RESET} Analyzing {NeonColors.BOLD}{total_articles}{NeonColors.RESET} articles...\n")
    
    # Analyze trending topics
    word_freq = analyze_trending_topics(articles, top_n=10)
    
    # Identify clusters
    clusters = identify_clusters(word_freq)
    
    # Print results to terminal
    print_trending_topics(word_freq, top_n=10)
    print_clusters(clusters)
    
    # Export to Markdown
    print(f"\n{NeonColors.CYAN}{'─' * 78}{NeonColors.RESET}\n")
    export_to_markdown(data, word_freq, clusters, 'output/intelligence_summary.md')
    
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.GREEN}[COMPLETE]{NeonColors.RESET} Analysis finished successfully")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{NeonColors.YELLOW}[ABORT]{NeonColors.RESET} Analysis interrupted")
    except Exception as e:
        print(f"\n{NeonColors.RED}[FATAL]{NeonColors.RESET} {e}")

