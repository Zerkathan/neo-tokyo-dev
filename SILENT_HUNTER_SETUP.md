# 🎯 Silent Hunter - Setup Guide

## 🚀 **Get Started in 5 Minutes**

Tu primer vigilante digital listo para detectar oportunidades 24/7.

---

## 📋 **Prerequisites Checklist**

```
□ Python 3.7+ installed
□ Telegram app installed
□ 5 minutes of time
```

---

## 🤖 **STEP 1: Create Telegram Bot (2 minutes)**

### **1.1 - Talk to BotFather:**
```
1. Open Telegram
2. Search for: @BotFather
3. Start chat
4. Send: /newbot
5. Follow prompts:
   - Bot name: "My Silent Hunter"
   - Username: "my_silent_hunter_bot" (must end in 'bot')
6. SAVE THE TOKEN! 
   Example: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### **1.2 - Get Your Chat ID:**
```
1. Search for: @userinfobot
2. Start chat
3. Bot will reply with your ID
4. SAVE YOUR ID!
   Example: 987654321
```

---

## ⚙️ **STEP 2: Configure Silent Hunter (1 minute)**

### **Edit `silent_hunter.py` lines 31-32:**

```python
# BEFORE:
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

# AFTER:
TELEGRAM_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  # Your token
TELEGRAM_CHAT_ID = "987654321"  # Your chat ID
```

### **Or use environment variables:**
```bash
# Windows PowerShell:
$env:TELEGRAM_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
$env:TELEGRAM_CHAT_ID="987654321"
python silent_hunter.py

# Linux/Mac:
export TELEGRAM_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
export TELEGRAM_CHAT_ID="987654321"
python silent_hunter.py
```

---

## 🎯 **STEP 3: Configure Your Target (1 minute)**

### **Edit lines 26-29:**

```python
# Example: Monitor RTX 4090 on Amazon
TARGET_URL = "https://www.amazon.com/dp/B0B16YLLH7"
PRICE_SELECTOR = "span.a-price-whole"
STOCK_SELECTOR = "#availability span"
TARGET_PRICE = 1500.0  # Alert if price drops below $1,500
```

### **How to find selectors:**
```
1. Open product page in browser
2. Right-click on price → Inspect
3. Right-click on element in DevTools → Copy → Copy selector
4. Paste into PRICE_SELECTOR

Same for stock/availability element.
```

---

## 🚀 **STEP 4: Run Silent Hunter (1 minute)**

### **Install dependencies:**
```bash
pip install requests beautifulsoup4
```

### **Start monitoring:**
```bash
python silent_hunter.py
```

### **Expected output:**
```
══════════════════════════════════════════════════════════════
🎯 SILENT HUNTER - Starting Monitoring
══════════════════════════════════════════════════════════════

🔗 Target: https://www.amazon.com/dp/...
💰 Target Price: $1500.00
⏱️ Check Interval: 60s
📱 Telegram: ✅ Configured

🟢 Monitoring started. Press Ctrl+C to stop.

────────────────────────────────────────────────────────────

[CYCLE #1] 15:30:00
────────────────────────────────────────────────────────────
🔍 Fetching: https://www.amazon.com/dp/...
✅ Status: 200
💰 Price extracted: $1,599.00
📦 Stock: AVAILABLE
✅ Check complete

⏳ Waiting 60s until next check...

[CYCLE #2] 15:31:00
────────────────────────────────────────────────────────────
🔍 Fetching: https://www.amazon.com/dp/...
✅ Status: 200
💰 Price extracted: $1,499.00
📦 Stock: AVAILABLE
🚨 ALERTS SENT: Price Drop
📨 Telegram alert sent!
✅ Check complete
```

---

## 📱 **STEP 5: Test Telegram Alert**

You should receive a message like:

```
🎯💰 PRICE ALERT!

💵 Current Price: $1,499.00
🎯 Target Price: $1500.00
📊 Status: ✅ BELOW TARGET!

🔗 View Product
⏰ 2025-12-05 15:31:00
```

---

## 🎯 **Quick Configuration Examples**

### **Example 1: GPU Monitor (NVIDIA RTX 4090)**
```python
TARGET_URL = "https://www.amazon.com/dp/B0B16YLLH7"
PRICE_SELECTOR = "span.a-price-whole"
STOCK_SELECTOR = "#availability span"
TARGET_PRICE = 1500.0
CHECK_INTERVAL = 60
```

### **Example 2: PlayStation 5 Stock Watcher**
```python
TARGET_URL = "https://www.bestbuy.com/site/sony-playstation-5/6426149.p"
PRICE_SELECTOR = ".priceView-customer-price span"
STOCK_SELECTOR = ".fulfillment-add-to-cart-button"
TARGET_PRICE = 500.0
CHECK_INTERVAL = 30  # Check every 30s (more aggressive)
```

### **Example 3: Sneaker Drop Monitor**
```python
TARGET_URL = "https://www.nike.com/t/air-jordan-1/..."
PRICE_SELECTOR = ".product-price"
STOCK_SELECTOR = ".product-availability"
TARGET_PRICE = 200.0
CHECK_INTERVAL = 120  # Check every 2 min
```

---

## 🔧 **Customization**

### **Change Check Interval:**
```python
CHECK_INTERVAL = 30   # Every 30 seconds (aggressive)
CHECK_INTERVAL = 60   # Every 1 minute (balanced)
CHECK_INTERVAL = 300  # Every 5 minutes (conservative)
```

### **Adjust Price Threshold:**
```python
TARGET_PRICE = 1500.0   # Alert when price <= $1,500
TARGET_PRICE = 1200.0   # Alert when price <= $1,200
```

### **Modify Alert Message:**
```python
# In send_alert() method, customize message format:
message = f"""
🚨 CUSTOM ALERT!

Product: {self.url}
Price: ${current_price}
Status: DEAL DETECTED!

Action: BUY NOW!
"""
```

---

## 🐛 **Troubleshooting**

### **Issue: "Telegram not configured"**
```
Solution:
1. Check you set TELEGRAM_TOKEN correctly
2. Check you set TELEGRAM_CHAT_ID correctly
3. Remove quotes if copying from terminal
4. Ensure no extra spaces
```

### **Issue: "Price element not found"**
```
Solution:
1. Website structure changed → Update selector
2. Test selector in browser console:
   document.querySelector("span.a-price-whole")
3. Try alternative selectors:
   - Look for data attributes: [data-price]
   - Try parent elements: .price-container span
   - Use XPath instead of CSS
```

### **Issue: "HTTP Error 403"**
```
Solution:
1. Site blocking bot → User-Agent rotation working
2. Try accessing URL in browser first
3. Check if site has anti-bot protection
4. Consider using proxies (advanced)
```

### **Issue: "Connection timeout"**
```
Solution:
1. Check internet connection
2. Site might be down temporarily
3. Bot will retry with exponential backoff
4. Increase timeout in fetch_page() if needed
```

---

## 💡 **Pro Tips**

### **1. Test Before Production:**
```bash
# Set a high target price to trigger alert immediately
TARGET_PRICE = 9999.0  # Will always alert

# Run once to test Telegram
python silent_hunter.py
# Stop with Ctrl+C after first cycle
```

### **2. Run in Background (Windows):**
```powershell
Start-Process python -ArgumentList "silent_hunter.py" -WindowStyle Hidden
```

### **3. Run in Background (Linux/Mac):**
```bash
nohup python silent_hunter.py > silent_hunter.log 2>&1 &

# Check if running:
ps aux | grep silent_hunter

# Stop:
kill $(pgrep -f silent_hunter)
```

### **4. Multiple Products:**
```bash
# Run multiple instances with different configs
# Copy silent_hunter.py to silent_hunter_gpu.py
# Copy silent_hunter.py to silent_hunter_ps5.py
# Edit each with different target
# Run both simultaneously
```

### **5. Monitor Your Monitor:**
```bash
# Create a watchdog for Silent Hunter
# If Silent Hunter crashes, restart it
while true; do
    python silent_hunter.py
    echo "Silent Hunter crashed, restarting in 5s..."
    sleep 5
done
```

---

## 🎓 **Graduation Path**

### **Level 1: Silent Hunter** ✅ (You are here)
```
✅ Monitor ONE product
✅ Telegram alerts
✅ Simple and focused
```

### **Level 2: Sniper Bot** (Next)
```
🔜 Monitor MULTIPLE products
🔜 Telegram + Discord
🔜 SQLite history
🔜 4 detection types
```

### **Level 3: Enterprise** (Future)
```
🔜 Web dashboard
🔜 User management
🔜 API access
🔜 Machine learning predictions
🔜 Auto-purchasing (advanced!)
```

---

## 🎊 **Success Checklist**

```
✅ Telegram bot created (@BotFather)
✅ Chat ID obtained (@userinfobot)
✅ Script configured (token + chat ID)
✅ Target configured (URL + selectors)
✅ Dependencies installed (requests, bs4)
✅ First run successful
✅ Test alert received
✅ Running in background

🎯 You're now hunting opportunities 24/7!
```

---

## 📞 **Support**

### **Can't find CSS selector?**
- Use SelectorGadget browser extension
- Post in GitHub issues with screenshot
- Check SILENT_HUNTER_SETUP.md examples

### **Telegram not working?**
- Verify bot token from @BotFather
- Verify chat ID from @userinfobot
- Send message to bot first
- Check internet connection

### **Getting blocked?**
- Increase CHECK_INTERVAL (60 → 120)
- Add random delays: time.sleep(random.randint(60, 90))
- Consider using proxies (advanced)

---

## 🎊 **Conclusion**

In 5 minutes, you've deployed a **24/7 vigilante** that:
- ✅ Never sleeps
- ✅ Never misses opportunities
- ✅ Alerts you instantly
- ✅ Costs $0.00 to run

**Welcome to the hunt, Cyberrunner.** 🎯⚡

---

**Powered by: Neo-Tokyo Dev v3.0**  
**Your competitive advantage starts now.** 💰

