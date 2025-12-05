# 🔮 Intelligence Pipeline - Complete Guide

## 🎯 **Overview**

Sistema completo de inteligencia automatizada con 3 componentes:

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  INFO-HARVESTER │  →   │     ANALYST     │  →   │    WATCHDOG     │
│   (El Cuerpo)   │      │  (El Cerebro)   │      │   (El Guardián) │
└─────────────────┘      └─────────────────┘      └─────────────────┘
   Scrapes data          Analyzes trends         Monitors & alerts
```

---

## 🚀 **Quick Start**

### **Método 1: Pipeline Manual**

```bash
# Paso 1: Recolectar datos
python output/info_harvester.py
# Output: intelligence_report.json

# Paso 2: Analizar datos
python output/analyst.py
# Output: intelligence_summary.md

# Paso 3: Leer resumen
cat output/intelligence_summary.md
```

### **Método 2: Pipeline Automatizada (Watchdog)**

```bash
# Single scan (testing)
python output/watchdog.py --once

# Continuous monitoring (production)
python output/watchdog.py
# Press Ctrl+C to stop
```

---

## 📦 **Component 1: Info-Harvester**

### **Purpose:**
Scrape tech news from Hacker News and TechCrunch.

### **Features:**
- ✅ Async scraping (aiohttp)
- ✅ BeautifulSoup parsing
- ✅ User-Agent rotation
- ✅ Rate limiting
- ✅ JSON export

### **Usage:**
```bash
python output/info_harvester.py
```

### **Output:**
```json
{
  "metadata": {
    "harvested_at": "2025-12-05T02:31:36",
    "total_articles": 10,
    "sources": ["Hacker News", "TechCrunch"]
  },
  "articles": [
    {
      "title": "AV1: A Modern, Open Codec",
      "url": "https://...",
      "score": 268,
      "source": "Hacker News",
      "timestamp": "2025-12-05T02:31:36"
    }
  ]
}
```

### **Configuration:**
Edit `info_harvester.py`:
```python
# Add more sources
async def scrape_reddit(...):
    # Your implementation
```

---

## 📊 **Component 2: Analyst**

### **Purpose:**
Analyze intelligence_report.json to extract insights.

### **Features:**
- ✅ Keyword extraction
- ✅ Frequency analysis
- ✅ Thematic clustering
- ✅ Markdown report
- ✅ No external dependencies

### **Usage:**
```bash
python output/analyst.py
```

### **Output (Terminal):**
```
══════════════════════════════════════════════════════════════
📊 TOP 10 TRENDING TOPICS
══════════════════════════════════════════════════════════════

[ 1] ai                   ████████ 4
[ 2] python               ██████ 3
[ 3] security             ████ 2
```

### **Output (Markdown):**
```markdown
# 🧠 Intelligence Summary Report

## 🔥 Top 10 Trending Topics
1. **ai** `▓▓▓▓▓▓▓▓` (4 mentions)
2. **python** `▓▓▓▓▓▓` (3 mentions)

## 🎯 Thematic Analysis
### 🤖 AI & Machine Learning (5 mentions)
- **ai**: 4 mentions
- **machine**: 1 mention
```

### **Configuration:**
Edit `analyst.py`:
```python
# Add custom stopwords
STOPWORDS.add('custom_word')

# Add custom clusters
clusters["🔥 Your Cluster"] = []
```

---

## 🐕 **Component 3: Watchdog**

### **Purpose:**
Automated monitoring with keyword alerts.

### **Features:**
- ✅ Auto-execution of pipeline
- ✅ Keyword detection
- ✅ Sound alerts
- ✅ Desktop notifications (Windows)
- ✅ Configurable intervals
- ✅ Loop mode + single scan mode

### **Usage:**

**Testing:**
```bash
python output/watchdog.py --once
```

**Production (run in background):**
```bash
# Windows
start /B python output/watchdog.py

# Linux/Mac
nohup python output/watchdog.py &
```

### **Configuration:**
Edit `watchdog.py`:
```python
CONFIG = {
    # YOUR KEYWORDS HERE
    "watch_keywords": [
        "ai", "gpt", "llm",
        "rust", "python",
        "crypto", "bitcoin",
        "security", "vulnerability",
    ],
    
    # Minimum mentions to trigger alert
    "alert_threshold": 2,
    
    # Scan every X seconds
    "scan_interval": 300,  # 5 minutes
    
    # Enable/disable features
    "sound_alerts": True,
    "desktop_notifications": True,
}
```

### **Output:**
```
🚨 ALERT: 'ai' DETECTED! 🚨
[ALERT] Found 3 mentions
[ALERT] Related articles:
  1. GPT-5 Released
  2. AI Regulation in EU
  3. Machine Learning Advances
[BEEP] 🔊
```

---

## 🎯 **Use Cases**

### **1. Track AI Trends**
```python
# watchdog.py
CONFIG = {
    "watch_keywords": ["ai", "gpt", "claude", "gemini", "llm"],
    "alert_threshold": 1,
    "scan_interval": 180,  # 3 minutes
}
```

### **2. Monitor Your Tech Stack**
```python
CONFIG = {
    "watch_keywords": ["python", "fastapi", "postgresql", "react"],
    "alert_threshold": 2,
    "scan_interval": 600,  # 10 minutes
}
```

### **3. Security Watch**
```python
CONFIG = {
    "watch_keywords": [
        "vulnerability", "cve", "exploit", "breach",
        "security", "hack", "ransomware"
    ],
    "alert_threshold": 1,  # Alert immediately
    "scan_interval": 120,  # 2 minutes
}
```

### **4. Startup/Business Intelligence**
```python
CONFIG = {
    "watch_keywords": [
        "startup", "funding", "series", "acquisition",
        "ipo", "valuation", "unicorn"
    ],
    "alert_threshold": 2,
    "scan_interval": 300,
}
```

---

## 🔧 **Customization**

### **Add New News Sources**

Edit `info_harvester.py`:
```python
async def scrape_reddit(session, semaphore):
    url = "https://reddit.com/r/programming"
    # Your scraping logic here
    return articles

# Add to main:
tasks = [
    fetch_hacker_news(...),
    fetch_techcrunch(...),
    scrape_reddit(...),  # NEW
]
```

### **Add Custom Thematic Clusters**

Edit `analyst.py`:
```python
cluster_keywords = {
    "🔥 Your Custom Cluster": ['keyword1', 'keyword2'],
}
```

### **Add Email Alerts**

Edit `watchdog.py`:
```python
import smtplib

def send_email_alert(keyword, count):
    # Your SMTP logic
    pass

# In alert():
send_email_alert(keyword, count)
```

---

## 📊 **Performance**

### **Benchmarks:**
```
Info-Harvester:
  - 2 sources: ~5-10 seconds
  - 10 articles average

Analyst:
  - 10 articles: <1 second
  - No external dependencies

Watchdog:
  - Full pipeline: ~10-15 seconds
  - Memory: <50 MB
```

### **Scaling:**
```python
# For larger datasets:
# 1. Use async.gather with more sources
# 2. Implement caching
# 3. Use SQLite for historical data
# 4. Add rate limiting per source
```

---

## 🐛 **Troubleshooting**

### **Problem: 403 Forbidden**
```
Solution: Website blocking requests
- Increase User-Agent rotation
- Add delays between requests
- Use proxies
- Consider headless browsers (Selenium)
```

### **Problem: No alerts triggered**
```
Solution: Lower threshold
CONFIG = {
    "alert_threshold": 1,  # Try 1 instead of 2
}
```

### **Problem: Too many alerts**
```
Solution: Increase threshold or interval
CONFIG = {
    "alert_threshold": 3,
    "scan_interval": 600,  # 10 minutes
}
```

---

## 🎓 **Learning Path**

### **Beginner:**
1. Run `info_harvester.py` manually
2. Read `intelligence_report.json`
3. Run `analyst.py` manually
4. Read `intelligence_summary.md`

### **Intermediate:**
1. Run `watchdog.py --once`
2. Modify `CONFIG` keywords
3. Test alerts

### **Advanced:**
1. Add new news sources
2. Customize thematic clusters
3. Implement email/Slack alerts
4. Create web dashboard
5. Store historical data in SQLite

---

## 🌟 **Best Practices**

### **1. Rate Limiting**
```python
# Respect robots.txt
# Add delays between requests
await asyncio.sleep(2)
```

### **2. Error Handling**
```python
try:
    result = await scrape_source()
except Exception as e:
    logger.error(f"Failed: {e}")
    continue  # Don't crash entire pipeline
```

### **3. Monitoring**
```python
# Log everything
# Track scan counts
# Monitor success rates
```

### **4. Data Retention**
```python
# Archive old reports
# Keep last 30 days
# Implement cleanup job
```

---

## 🚀 **Next Steps**

### **Enhancements:**
1. **Web Dashboard** - Flask/FastAPI UI
2. **Database** - SQLite for historical trends
3. **More Sources** - Reddit, Twitter, RSS feeds
4. **Sentiment Analysis** - NLP for article sentiment
5. **Telegram Bot** - Mobile alerts
6. **API** - Expose as REST API
7. **Docker** - Containerize pipeline
8. **Scheduling** - Cron/Task Scheduler integration

---

## 📚 **Resources**

### **Dependencies:**
```bash
pip install aiohttp beautifulsoup4
```

### **Files:**
```
output/
├── info_harvester.py     (300 lines)
├── analyst.py            (300 lines)
├── watchdog.py           (350 lines)
├── intelligence_report.json
└── intelligence_summary.md
```

### **GitHub:**
https://github.com/Zerkathan/neo-tokyo-dev

---

## 🎊 **Conclusion**

Tienes un sistema completo de inteligencia:
- 🕷️ Scrapes datos automáticamente
- 🧠 Analiza tendencias
- 🐕 Monitorea keywords
- 🚨 Alerta en tiempo real

**¡La Matrix está bajo tu control!** 🔮

---

**Powered by: Neo-Tokyo Dev v3.0 Golden Stack**  
**Generado con: Llama 3.1 + Qwen 2.5 Coder**

