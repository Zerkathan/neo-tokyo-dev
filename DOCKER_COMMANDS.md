# 🐳 Docker Commands Reference

## 🚀 **Quick Start**

```bash
# 1. Create .env file
cp .env.example .env
# Edit .env with your tokens

# 2. Build and run
docker-compose up -d

# 3. View logs
docker-compose logs -f sniper-bot

# 4. Stop
docker-compose down
```

---

## 📋 **Essential Commands**

### **Build:**
```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build sniper-bot

# Build without cache (fresh build)
docker-compose build --no-cache
```

### **Run:**
```bash
# Start in background (detached)
docker-compose up -d

# Start in foreground (see logs)
docker-compose up

# Start specific service
docker-compose up -d sniper-bot
```

### **Logs:**
```bash
# View logs (all services)
docker-compose logs

# Follow logs (real-time)
docker-compose logs -f

# Logs for specific service
docker-compose logs -f sniper-bot

# Last 100 lines
docker-compose logs --tail=100 sniper-bot
```

### **Stop:**
```bash
# Stop all services
docker-compose stop

# Stop specific service
docker-compose stop sniper-bot

# Stop and remove containers
docker-compose down

# Stop, remove, and delete volumes
docker-compose down -v
```

### **Restart:**
```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart sniper-bot
```

### **Status:**
```bash
# List running containers
docker-compose ps

# Detailed status
docker ps
```

---

## 🔧 **Management Commands**

### **Enter Container:**
```bash
# Open shell in running container
docker-compose exec sniper-bot /bin/bash

# Or use sh if bash not available
docker-compose exec sniper-bot /bin/sh

# Run command without entering
docker-compose exec sniper-bot python sniper_bot.py stats
```

### **Update Code:**
```bash
# 1. Edit your code
# 2. Rebuild and restart
docker-compose up -d --build

# Or:
docker-compose down
docker-compose up -d --build
```

### **View Resource Usage:**
```bash
# Real-time stats
docker stats

# Stats for specific container
docker stats neo-tokyo-sniper-bot
```

---

## 🐛 **Debugging Commands**

### **Check Logs for Errors:**
```bash
# Last 50 lines
docker-compose logs --tail=50 sniper-bot

# Search logs
docker-compose logs sniper-bot | grep ERROR

# With timestamps
docker-compose logs -t sniper-bot
```

### **Test Configuration:**
```bash
# Run single check
docker-compose run --rm sniper-bot python sniper_bot.py check

# View stats
docker-compose run --rm sniper-bot python sniper_bot.py stats
```

### **Inspect Container:**
```bash
# Get container details
docker inspect neo-tokyo-sniper-bot

# Check environment variables
docker inspect neo-tokyo-sniper-bot | grep -A 20 Env

# Check volumes
docker inspect neo-tokyo-sniper-bot | grep -A 10 Mounts
```

---

## 🧹 **Cleanup Commands**

### **Remove Old Images:**
```bash
# Remove unused images
docker image prune

# Remove all unused images
docker image prune -a

# Free up space
docker system prune
```

### **Remove Containers:**
```bash
# Remove stopped containers
docker container prune

# Remove all containers (dangerous!)
docker rm -f $(docker ps -aq)
```

### **Complete Cleanup:**
```bash
# Remove everything (be careful!)
docker-compose down -v
docker system prune -a --volumes
```

---

## 🚀 **Production Commands**

### **Deploy to Server:**
```bash
# 1. Copy files to server
scp -r . user@server:/opt/neo-tokyo/

# 2. SSH into server
ssh user@server

# 3. Navigate and start
cd /opt/neo-tokyo/
docker-compose up -d

# 4. Verify
docker-compose ps
docker-compose logs -f
```

### **Auto-start on Boot:**
```bash
# Docker service should auto-start containers with restart: always

# Verify Docker auto-start:
sudo systemctl enable docker

# Containers will auto-start after reboot
```

### **Update in Production:**
```bash
# 1. Pull latest code
git pull origin master

# 2. Rebuild and restart with zero downtime
docker-compose up -d --build --no-deps sniper-bot
```

---

## 📊 **Monitoring Commands**

### **Check Health:**
```bash
# View health status
docker-compose ps

# Check container health
docker inspect --format='{{.State.Health.Status}}' neo-tokyo-sniper-bot
```

### **Resource Monitoring:**
```bash
# Live resource usage
docker stats neo-tokyo-sniper-bot

# CPU and memory
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

---

## 💡 **Pro Tips**

### **1. Development vs Production:**
```yaml
# docker-compose.override.yml (auto-loaded, for dev)
services:
  sniper-bot:
    volumes:
      - .:/app  # Live code reload
    command: python sniper_bot.py check  # Single check for testing
```

### **2. Multiple Environments:**
```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### **3. Backup Database:**
```bash
# Copy from container
docker cp neo-tokyo-sniper-bot:/app/sniper_history.db ./backup_$(date +%Y%m%d).db
```

### **4. Run Multiple Services:**
```bash
# Start all Neo-Tokyo services
docker-compose up -d sniper-bot intelligence-dashboard command-center
```

---

## 🎊 **Complete Workflow**

```bash
# Initial setup
cp .env.example .env
# Edit .env with your tokens
nano .env

# Build
docker-compose build

# Start in background
docker-compose up -d

# Check logs
docker-compose logs -f sniper-bot

# Verify running
docker-compose ps

# Check stats
docker-compose exec sniper-bot python sniper_bot.py stats

# Update config
nano sniper_config.json

# Restart to apply changes
docker-compose restart sniper-bot

# View logs for errors
docker-compose logs --tail=100 sniper-bot | grep ERROR

# Stop when done
docker-compose down
```

---

## 🎯 **Success Checklist**

```
✅ .env file created and configured
✅ Docker and docker-compose installed
✅ docker-compose build successful
✅ docker-compose up -d running
✅ docker-compose ps shows "Up"
✅ docker-compose logs shows activity
✅ Test alert received on Telegram
✅ Service survives reboot (restart: always)

🎊 Your Sniper Bot is now a professional service!
```

---

**Powered by: Neo-Tokyo Dev v3.0**  
**From script to service in minutes.** 🐳⚡

