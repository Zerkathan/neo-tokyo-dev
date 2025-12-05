# 🌐 Intelligence Dashboard - Quick Start Guide

## 🎯 Overview

Sistema web completo para visualizar intelligence data en tiempo real con dashboard Cyberpunk.

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   SQLite DB      │ ←── │  FastAPI Backend │ ←── │  HTML/CSS/JS     │
│  intelligence.db │     │     app.py       │     │    Dashboard     │
└──────────────────┘     └──────────────────┘     └──────────────────┘
  Historical data        REST API endpoints      Chart.js visualizations
```

---

## 🚀 Quick Start

### **Step 1: Initialize Database**
```bash
python database_manager.py
```

Output:
```
✅ Database initialized: intelligence.db
✅ Scan saved: ID=1, Articles=10, Keywords=60
```

### **Step 2: Start Server**
```bash
python app.py
```

Output:
```
🚀 Server: http://localhost:8000
📊 Dashboard: http://localhost:8000/
📡 API Docs: http://localhost:8000/docs
```

### **Step 3: Open Dashboard**
Navigate to: **http://localhost:8000**

---

## 📊 Dashboard Features

### **Real-time Stats Cards:**
- ✅ Total Scans
- ✅ Total Articles
- ✅ Unique Keywords
- ✅ Last Scan Time

### **Trending Topics Chart:**
- ✅ Bar chart with Chart.js
- ✅ Top 10 keywords (last 7 days)
- ✅ Neon colors (Cyberpunk style)

### **Latest Articles List:**
- ✅ Real-time article feed
- ✅ Scores and sources
- ✅ Direct links to articles

### **Auto-refresh:**
- ✅ Updates every 30 seconds
- ✅ No page reload needed

---

## 🔧 Architecture

### **Database Schema (SQLite):**

```sql
-- Scans table
CREATE TABLE scans (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    source TEXT NOT NULL,
    total_articles INTEGER NOT NULL
);

-- Articles table
CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    scan_id INTEGER REFERENCES scans(id),
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    score INTEGER,
    source TEXT NOT NULL,
    timestamp DATETIME NOT NULL
);

-- Keywords table
CREATE TABLE keywords (
    id INTEGER PRIMARY KEY,
    scan_id INTEGER REFERENCES scans(id),
    keyword TEXT NOT NULL,
    frequency INTEGER NOT NULL
);
```

### **API Endpoints:**

```
GET  /                  → Dashboard HTML
GET  /api/latest        → Latest articles
GET  /api/trends        → Trending keywords
GET  /api/history       → Scan history
GET  /api/stats         → Statistics
POST /api/scan          → Save new scan
GET  /docs              → API documentation (Swagger)
```

---

## 📡 API Usage

### **Get Latest Articles:**
```bash
curl http://localhost:8000/api/latest?limit=10
```

Response:
```json
{
  "success": true,
  "count": 10,
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

### **Get Trending Keywords:**
```bash
curl http://localhost:8000/api/trends?days=7&limit=10
```

Response:
```json
{
  "success": true,
  "period_days": 7,
  "count": 5,
  "trends": [
    {"keyword": "modern", "frequency": 2},
    {"keyword": "years", "frequency": 2}
  ]
}
```

### **Get Statistics:**
```bash
curl http://localhost:8000/api/stats
```

Response:
```json
{
  "success": true,
  "stats": {
    "total_scans": 1,
    "total_articles": 10,
    "total_keywords": 20,
    "last_scan": "2025-12-05T02:31:36.636419"
  }
}
```

---

## 🎨 Cyberpunk Style

### **Color Palette:**
```css
Background: #0a0e27 → #1a1f3a (gradient)
Primary:    #00ff9f (neon green)
Secondary:  #ff00ff (neon magenta)
Accent:     #00d4ff (neon cyan)
```

### **Features:**
- ✅ Dark background gradient
- ✅ Neon borders and glows
- ✅ Monospace font (Courier New)
- ✅ Smooth hover effects
- ✅ Pulsing refresh indicator
- ✅ Custom scrollbars

---

## 🔄 Integration with Pipeline

### **Manual Integration:**
```bash
# 1. Harvest data
python output/info_harvester.py

# 2. Save to database
python database_manager.py

# 3. Dashboard auto-updates
# (via API calls every 30s)
```

### **Automated Integration (Watchdog + Dashboard):**

Modify `watchdog.py`:
```python
# After save_artifacts():
import database_manager as db
db.save_scan('output/intelligence_report.json')
print("[DB] Scan saved to dashboard")
```

---

## 📈 Advanced Features

### **Historical Trends:**
Query trends over different time periods:
```bash
# Last 7 days
curl http://localhost:8000/api/trends?days=7

# Last 30 days
curl http://localhost:8000/api/trends?days=30

# Last 90 days
curl http://localhost:8000/api/trends?days=90
```

### **Scan History:**
```bash
curl http://localhost:8000/api/history?days=30
```

### **Export Data:**
Use database_manager.py functions:
```python
import database_manager as db

# Get all trends
trends = db.get_trends(days=30, limit=100)

# Get all articles
articles = db.get_latest(limit=1000)

# Export to JSON
import json
with open('export.json', 'w') as f:
    json.dump({'trends': trends, 'articles': articles}, f)
```

---

## 🔧 Customization

### **Change Auto-refresh Interval:**

Edit `templates/index.html`:
```javascript
// Change from 30s to 60s
setInterval(updateAll, 60000);
```

### **Add More Stats:**

Edit `database_manager.py`:
```python
def get_stats():
    # Add new stat
    cursor.execute('SELECT AVG(score) FROM articles')
    avg_score = cursor.fetchone()[0]
    
    return {
        # ... existing stats
        'avg_score': avg_score
    }
```

### **Customize Chart:**

Edit `templates/index.html`:
```javascript
// Change to line chart
trendsChart = new Chart(ctx, {
    type: 'line',  // Changed from 'bar'
    // ... rest of config
});
```

---

## 🐛 Troubleshooting

### **Problem: Database not found**
```bash
Solution: Initialize database first
python database_manager.py
```

### **Problem: Port 8000 already in use**
```bash
Solution: Change port in app.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### **Problem: Dashboard shows "No articles"**
```bash
Solution: Save a scan first
python database_manager.py
```

### **Problem: CORS errors**
```
Solution: Already configured in app.py
CORSMiddleware allows all origins (for development)
```

---

## 🚀 Deployment

### **Production Checklist:**
- ✅ Change CORS origins to specific domains
- ✅ Add authentication (JWT)
- ✅ Use environment variables for config
- ✅ Enable HTTPS
- ✅ Use production ASGI server (gunicorn + uvicorn)
- ✅ Set up reverse proxy (nginx)
- ✅ Database backups

### **Docker Deployment:**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements_dashboard.txt .
RUN pip install -r requirements_dashboard.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
```

---

## 📚 Tech Stack

```
Backend:
  - FastAPI (REST API)
  - SQLite (Database)
  - Uvicorn (ASGI server)

Frontend:
  - HTML5/CSS3
  - Vanilla JavaScript
  - Chart.js (visualizations)

Integration:
  - database_manager.py (ORM)
  - info_harvester.py (data source)
```

---

## 🎓 Next Steps

1. **Add authentication** (JWT tokens)
2. **Real-time updates** (WebSockets)
3. **More visualizations** (pie charts, time series)
4. **Export functionality** (CSV, PDF reports)
5. **User preferences** (dark/light mode, chart types)
6. **Alert system** (email notifications)
7. **API rate limiting**
8. **Caching** (Redis)

---

## 🎊 Conclusion

Tienes un **Dashboard Web completo** con:
- 🌐 Interface Cyberpunk moderna
- 📊 Visualizaciones en tiempo real
- 💾 Histórico persistente
- 🚀 API REST documentada
- ⚡ Auto-refresh cada 30s

**¡El futuro es ahora!** 🔮

---

**Powered by: Neo-Tokyo Dev v3.0 Golden Stack**  
**Generated with: Llama 3.1 + Qwen 2.5 Coder**

