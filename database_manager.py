#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  💾 DATABASE MANAGER - SQLite Intelligence Storage                          ║
║  Manages historical intelligence data in SQLite                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


DATABASE_PATH = "intelligence.db"


# ══════════════════════════════════════════════════════════════════════════════
# 🗄️ DATABASE SCHEMA
# ══════════════════════════════════════════════════════════════════════════════

def init_db():
    """Initialize SQLite database with schema."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Table: scans (each harvest run)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            source TEXT NOT NULL,
            total_articles INTEGER NOT NULL
        )
    ''')
    
    # Table: articles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            score INTEGER,
            source TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            FOREIGN KEY (scan_id) REFERENCES scans (id)
        )
    ''')
    
    # Table: keywords
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id INTEGER NOT NULL,
            keyword TEXT NOT NULL,
            frequency INTEGER NOT NULL,
            FOREIGN KEY (scan_id) REFERENCES scans (id)
        )
    ''')
    
    # Indices for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_articles_scan ON articles(scan_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_keywords_scan ON keywords(scan_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_scans_timestamp ON scans(timestamp)')
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized: {DATABASE_PATH}")


# ══════════════════════════════════════════════════════════════════════════════
# 💾 DATA OPERATIONS
# ══════════════════════════════════════════════════════════════════════════════

def save_scan(json_path: str = "output/intelligence_report.json") -> int:
    """
    Save intelligence report to database.
    Returns scan_id.
    """
    # Read JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {json_path}")
        return None
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Insert scan
    metadata = data.get('metadata', {})
    cursor.execute('''
        INSERT INTO scans (timestamp, source, total_articles)
        VALUES (?, ?, ?)
    ''', (
        metadata.get('harvested_at', datetime.now().isoformat()),
        ', '.join(metadata.get('sources', ['Unknown'])),
        metadata.get('total_articles', 0)
    ))
    
    scan_id = cursor.lastrowid
    
    # Insert articles
    articles = data.get('articles', [])
    for article in articles:
        cursor.execute('''
            INSERT INTO articles (scan_id, title, url, score, source, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            scan_id,
            article.get('title', 'Unknown'),
            article.get('url', ''),
            article.get('score', 0),
            article.get('source', 'Unknown'),
            article.get('timestamp', datetime.now().isoformat())
        ))
    
    # Calculate and insert keywords (basic frequency analysis)
    from collections import Counter
    import re
    
    # Extract words from titles
    all_words = []
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    for article in articles:
        title = article.get('title', '').lower()
        words = re.findall(r'\b\w{3,}\b', title)  # Words with 3+ chars
        words = [w for w in words if w not in stopwords]
        all_words.extend(words)
    
    word_freq = Counter(all_words)
    
    # Insert top 20 keywords
    for keyword, frequency in word_freq.most_common(20):
        cursor.execute('''
            INSERT INTO keywords (scan_id, keyword, frequency)
            VALUES (?, ?, ?)
        ''', (scan_id, keyword, frequency))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Scan saved: ID={scan_id}, Articles={len(articles)}, Keywords={len(word_freq)}")
    
    return scan_id


def get_latest(limit: int = 10) -> List[Dict]:
    """Get latest articles."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.title, a.url, a.score, a.source, a.timestamp
        FROM articles a
        JOIN scans s ON a.scan_id = s.id
        ORDER BY s.timestamp DESC, a.score DESC
        LIMIT ?
    ''', (limit,))
    
    articles = []
    for row in cursor.fetchall():
        articles.append({
            'title': row[0],
            'url': row[1],
            'score': row[2],
            'source': row[3],
            'timestamp': row[4]
        })
    
    conn.close()
    return articles


def get_trends(days: int = 7, limit: int = 10) -> List[Dict]:
    """Get trending keywords from last N days."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT k.keyword, SUM(k.frequency) as total_freq
        FROM keywords k
        JOIN scans s ON k.scan_id = s.id
        WHERE datetime(s.timestamp) >= datetime('now', '-' || ? || ' days')
        GROUP BY k.keyword
        ORDER BY total_freq DESC
        LIMIT ?
    ''', (days, limit))
    
    trends = []
    for row in cursor.fetchall():
        trends.append({
            'keyword': row[0],
            'frequency': row[1]
        })
    
    conn.close()
    return trends


def get_history(days: int = 30) -> List[Dict]:
    """Get scan history."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, timestamp, source, total_articles
        FROM scans
        WHERE datetime(timestamp) >= datetime('now', '-' || ? || ' days')
        ORDER BY timestamp DESC
    ''', (days,))
    
    history = []
    for row in cursor.fetchall():
        history.append({
            'id': row[0],
            'timestamp': row[1],
            'source': row[2],
            'total_articles': row[3]
        })
    
    conn.close()
    return history


def get_stats() -> Dict:
    """Get general statistics."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Total scans
    cursor.execute('SELECT COUNT(*) FROM scans')
    total_scans = cursor.fetchone()[0]
    
    # Total articles
    cursor.execute('SELECT COUNT(*) FROM articles')
    total_articles = cursor.fetchone()[0]
    
    # Unique keywords
    cursor.execute('SELECT COUNT(DISTINCT keyword) FROM keywords')
    total_keywords = cursor.fetchone()[0]
    
    # Last scan time
    cursor.execute('SELECT MAX(timestamp) FROM scans')
    last_scan = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_scans': total_scans,
        'total_articles': total_articles,
        'total_keywords': total_keywords,
        'last_scan': last_scan
    }


# ══════════════════════════════════════════════════════════════════════════════
# 🧪 MAIN (Testing)
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🗄️ Initializing database...")
    init_db()
    
    print("\n💾 Saving intelligence report...")
    scan_id = save_scan()
    
    if scan_id:
        print(f"\n📊 Scan saved with ID: {scan_id}")
        
        print("\n📰 Latest articles:")
        for i, article in enumerate(get_latest(5), 1):
            print(f"  {i}. {article['title'][:60]}...")
        
        print("\n🔥 Trending keywords (last 7 days):")
        for i, trend in enumerate(get_trends(7, 5), 1):
            print(f"  {i}. {trend['keyword']} ({trend['frequency']})")
        
        print("\n📈 Statistics:")
        stats = get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")

