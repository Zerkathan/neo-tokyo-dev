#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🌐 INTELLIGENCE DASHBOARD - FastAPI Backend                                ║
║  REST API for Intelligence Data Visualization                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import database_manager as db

# Initialize FastAPI
app = FastAPI(
    title="Intelligence Dashboard API",
    description="REST API for Neo-Tokyo Intelligence System",
    version="3.0.0"
)

# CORS (allow frontend to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on server start."""
    db.init_db()
    print("✅ Database initialized")


# ══════════════════════════════════════════════════════════════════════════════
# 🏠 FRONTEND
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the Intelligence Dashboard HTML."""
    html_path = Path("templates/index.html")
    
    if not html_path.exists():
        return HTMLResponse(
            content="<h1>Dashboard not found</h1><p>Please create templates/index.html</p>",
            status_code=404
        )
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    return HTMLResponse(content=html_content)


# ══════════════════════════════════════════════════════════════════════════════
# 📊 API ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/api/latest")
async def get_latest_articles(limit: int = 20):
    """
    Get latest articles.
    
    Query params:
    - limit: Number of articles to return (default: 20)
    """
    try:
        articles = db.get_latest(limit)
        return {
            "success": True,
            "count": len(articles),
            "articles": articles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/trends")
async def get_trending_keywords(days: int = 7, limit: int = 10):
    """
    Get trending keywords from last N days.
    
    Query params:
    - days: Number of days to look back (default: 7)
    - limit: Number of keywords to return (default: 10)
    """
    try:
        trends = db.get_trends(days, limit)
        return {
            "success": True,
            "period_days": days,
            "count": len(trends),
            "trends": trends
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
async def get_scan_history(days: int = 30):
    """
    Get scan history from last N days.
    
    Query params:
    - days: Number of days to look back (default: 30)
    """
    try:
        history = db.get_history(days)
        return {
            "success": True,
            "period_days": days,
            "count": len(history),
            "scans": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_statistics():
    """Get general database statistics."""
    try:
        stats = db.get_stats()
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/scan")
async def save_new_scan():
    """
    Trigger saving a new scan from intelligence_report.json.
    """
    try:
        scan_id = db.save_scan()
        if scan_id:
            return {
                "success": True,
                "scan_id": scan_id,
                "message": "Scan saved successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="intelligence_report.json not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ══════════════════════════════════════════════════════════════════════════════
# 🎯 MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║  🌐 INTELLIGENCE DASHBOARD - Starting Server...                      ║")
    print("╚══════════════════════════════════════════════════════════════════════╝\n")
    print("🚀 Server: http://localhost:8000")
    print("📊 Dashboard: http://localhost:8000/")
    print("📡 API Docs: http://localhost:8000/docs")
    print("\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

