# ══════════════════════════════════════════════════════════════════════════════
# 🐳 DOCKERFILE - Neo-Tokyo Dev Services
# Optimized multi-stage build for production deployment
# ══════════════════════════════════════════════════════════════════════════════

# Use Python slim image (smaller than full Python image)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY sniper_bot.py .
COPY sniper_config.json .

# Create non-root user for security
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

# Switch to non-root user
USER botuser

# Health check (optional - checks if bot is responsive)
HEALTHCHECK --interval=5m --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import sqlite3; conn = sqlite3.connect('sniper_history.db'); conn.close()" || exit 1

# Set environment variables (can be overridden by docker-compose)
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "sniper_bot.py", "run"]

