# 🚀 Advanced Use Cases - Escalando la Operación

## 🔮 Neo-Tokyo Dev v3.0 - Casos de Uso Avanzados

Una vez dominaste el **Info-Harvester** (Misión 2), es hora de apuntar tu "Taladro de Datos" a objetivos más valiosos.

---

## 📊 **CASO DE USO 3: Monitor de Precios (Arbitraje)**

### 🎯 **Objetivo:**
Scraper que monitorea precios de productos (ej: tarjetas gráficas RTX 4090) en múltiples tiendas cada 60 segundos y alerta cuando el precio baja del promedio histórico.

### 🏗️ **Arquitectura Propuesta:**

```python
# Estructura de datos
@dataclass
class PricePoint:
    product: str          # "RTX 4090"
    store: str           # "Amazon", "Newegg", "Best Buy"
    price: float         # 1599.99
    currency: str        # "USD"
    in_stock: bool       # True/False
    url: str             # Product URL
    timestamp: datetime  # When scraped
    
# Stores to monitor
STORES = {
    "Amazon": "https://www.amazon.com/s?k=rtx+4090",
    "Newegg": "https://www.newegg.com/p/pl?d=rtx+4090",
    "Best Buy": "https://www.bestbuy.com/site/searchpage.jsp?st=rtx+4090"
}
```

### 🎨 **Features:**
- ✅ **Async monitoring** de 3+ tiendas simultáneamente
- ✅ **Price history** guardado en SQLite o JSON
- ✅ **Alert system** cuando precio < promedio_histórico - 5%
- ✅ **Rate limiting** (60 segundos entre scrapes)
- ✅ **User-Agent rotation** para evitar baneos
- ✅ **Discord/Telegram webhook** para alertas en tiempo real
- ✅ **CSV export** para análisis de datos
- ✅ **Web dashboard** (opcional) con gráficos de tendencias

### 📝 **Prompt para Neo-Tokyo Dev:**

```
ARQUITECTO (Temp 0.85):
Diseña un sistema de monitoreo de precios en tiempo real llamado "Price-Sentinel".

1. Arquitectura de datos:
   - Define una estructura unificada para precios de diferentes tiendas
   - Diseña un sistema de almacenamiento histórico (SQLite o JSON timestamped)
   - Crea un algoritmo de detección de "buenas ofertas" (precio < promedio - threshold)

2. Sistema de alertas:
   - Cuando detecte un precio bajo, debe notificar vía terminal (logs neon)
   - Diseña webhooks opcionales (Discord/Telegram) para alertas móviles

3. Rate limiting inteligente:
   - Scraping cada 60 segundos por tienda
   - Semáforos para no saturar la red
   - Rotación de User-Agents

IMPLEMENTADOR (Temp 0.3):
Implementa Price-Sentinel en Python.

1. Stack obligatorio:
   - aiohttp + BeautifulSoup para scraping
   - asyncio para concurrencia
   - sqlite3 o JSON para almacenamiento
   - (Opcional) requests para webhooks

2. Funcionalidades:
   - async def monitor_store(store_name, url) -> PricePoint
   - def calculate_average(product, days=7) -> float
   - def detect_deal(current_price, avg_price, threshold=0.05) -> bool
   - async def send_alert(deal: PricePoint) -> None

3. Output:
   - Logs neon en tiempo real: "[PRICE] Amazon: $1,499 (↓ 6% vs avg)"
   - Alertas cuando precio < promedio: "[DEAL!] RTX 4090 @ Amazon: $1,499 (save $100)"
   - Guardar en: output/price_history.json o price_sentinel.db
```

### 🎬 **Ejecución esperada:**

```bash
python ai_duo.py "..." # Pegar el prompt

# El Dúo genera el código
# [SYSTEM] 💾 Artifact secured: output/price_sentinel.py

python output/price_sentinel.py

# Output:
# ══════════════════════════════════════════════════════════════
# 🔮 PRICE-SENTINEL - Monitoring 3 stores...
# ══════════════════════════════════════════════════════════════
# [FETCH] Amazon...
# [FETCH] Newegg...
# [FETCH] Best Buy...
# [PRICE] Amazon: $1,599 (→ 0% vs avg)
# [PRICE] Newegg: $1,649 (+3% vs avg)
# [DEAL!] Best Buy: $1,499 (↓ 6% vs avg) ⚡ ALERT SENT
# ══════════════════════════════════════════════════════════════
# [INFO] Next scan in 60 seconds...
```

---

## 💼 **CASO DE USO 4: Buscador de Empleos (Job-Hunter)**

### 🎯 **Objetivo:**
Scraper que busca ofertas de trabajo en LinkedIn, Indeed, y otros portales usando palabras clave específicas ("Python", "Remote", "Cyberpunk", "AI Engineer") y guarda resultados en CSV con deduplicación.

### 🏗️ **Arquitectura Propuesta:**

```python
# Estructura de datos
@dataclass
class JobListing:
    title: str           # "Senior Python Developer"
    company: str         # "OpenAI"
    location: str        # "Remote / San Francisco"
    salary: Optional[str] # "$150k - $200k" or None
    posted_date: str     # "2 days ago"
    url: str             # Job posting URL
    source: str          # "LinkedIn", "Indeed"
    keywords_matched: List[str]  # ["Python", "Remote"]
    timestamp: datetime  # When scraped
    
# Job boards to scrape
BOARDS = {
    "Indeed": "https://www.indeed.com/jobs?q={keywords}&l={location}",
    "LinkedIn": "https://www.linkedin.com/jobs/search?keywords={keywords}&location={location}",
    "RemoteOK": "https://remoteok.com/remote-{keywords}-jobs"
}

# Search config
SEARCH_CONFIG = {
    "keywords": ["Python", "AI Engineer", "Remote", "Cyberpunk"],
    "location": "Remote",
    "min_salary": 100000  # Filter jobs < $100k
}
```

### 🎨 **Features:**
- ✅ **Multi-board scraping** (Indeed, LinkedIn, RemoteOK)
- ✅ **Keyword matching** con scoring (más keywords = mejor match)
- ✅ **Deduplication** (evita guardar el mismo job 2 veces)
- ✅ **Salary parsing** (extrae rangos salariales)
- ✅ **CSV export** para análisis en Excel/Google Sheets
- ✅ **Email alerts** cuando encuentre jobs con score > 80%
- ✅ **Cron scheduling** (ejecutar cada 6 horas automáticamente)

### 📝 **Prompt para Neo-Tokyo Dev:**

```
ARQUITECTO (Temp 0.85):
Diseña un sistema de búsqueda de empleo automatizado llamado "Job-Hunter".

1. Arquitectura de datos:
   - Define estructura unificada JobListing para diferentes portales
   - Sistema de scoring: más keywords matched = mayor score (0-100)
   - Deduplicación: usar hash de (title + company) para evitar duplicados

2. Estrategia de scraping:
   - Scrape Indeed, LinkedIn, RemoteOK simultáneamente
   - Parsing inteligente de salarios ("$100k-$150k", "100000-150000", etc.)
   - Respeto de robots.txt y rate limiting

3. Alertas y export:
   - Guardar en CSV con columnas: title, company, location, salary, url, score, source
   - Alerta en terminal si score > 80%: "[MATCH!] Senior Python Dev @ OpenAI (95% match)"

IMPLEMENTADOR (Temp 0.3):
Implementa Job-Hunter en Python.

1. Stack:
   - aiohttp + BeautifulSoup (scraping)
   - csv module (export)
   - hashlib (deduplication)
   - re (salary parsing)

2. Funciones clave:
   - async def scrape_indeed(keywords, location) -> List[JobListing]
   - async def scrape_linkedin(keywords, location) -> List[JobListing]
   - def calculate_match_score(job: JobListing, search_config) -> int
   - def deduplicate_jobs(jobs: List[JobListing]) -> List[JobListing]
   - def export_to_csv(jobs: List[JobListing], filename: str)

3. Output:
   - Logs neon: "[FOUND] 15 jobs from Indeed, 23 from LinkedIn, 8 from RemoteOK"
   - CSV: output/job_listings_2025-12-05.csv
   - Alertas: "[MATCH!] AI Engineer @ DeepMind (92% match) - $180k-$220k"
```

### 🎬 **Ejecución esperada:**

```bash
python ai_duo.py "..." # Pegar el prompt

# El Dúo genera el código
# [SYSTEM] 💾 Artifact secured: output/job_hunter.py

python output/job_hunter.py

# Output:
# ══════════════════════════════════════════════════════════════
# 🔮 JOB-HUNTER - Searching for: Python, AI Engineer, Remote
# ══════════════════════════════════════════════════════════════
# [FETCH] Indeed...
# [FETCH] LinkedIn...
# [FETCH] RemoteOK...
# [FOUND] Indeed: 15 jobs
# [FOUND] LinkedIn: 23 jobs
# [FOUND] RemoteOK: 8 jobs
# [FILTER] Removing duplicates... (3 duplicates found)
# [FILTER] Applying salary filter ($100k+)... (12 jobs passed)
# 
# [MATCH!] Senior Python Engineer @ OpenAI (95% match)
#   Location: Remote
#   Salary: $180k - $220k
#   URL: https://openai.com/careers/...
# 
# [MATCH!] AI Engineer @ DeepMind (88% match)
#   Location: London / Remote
#   Salary: £120k - £160k
#   URL: https://deepmind.google/careers/...
# 
# ══════════════════════════════════════════════════════════════
# [SUCCESS] 43 jobs saved to: output/job_listings_2025-12-05.csv
# [STATS] 2 high-match jobs found (score > 80%)
# ══════════════════════════════════════════════════════════════
```

---

## 🌐 **OTROS CASOS DE USO AVANZADOS**

### 🏢 **5. Real Estate Monitor**
Monitorear propiedades en Zillow/Redfin por precio, ubicación, y características.

```python
# Alerta cuando:
# - Nueva propiedad < $500k en tu área
# - Precio reducido > 10%
# - Propiedad con palabras clave: "pool", "garage", "renovated"
```

### 📈 **6. Crypto Price Tracker**
Scraping de CoinMarketCap/CoinGecko para alertas de volatilidad.

```python
# Alerta cuando:
# - BTC sube/baja > 5% en 1 hora
# - Volumen de trading aumenta > 50%
# - Nuevas monedas listadas en exchanges top
```

### 📰 **7. Research Paper Aggregator**
Scraping de arXiv/Google Scholar por papers recientes en tu campo.

```python
# Buscar papers con keywords:
# - "transformer", "large language models", "reinforcement learning"
# - Filtrar por citaciones > 100
# - Guardar PDFs automáticamente
```

### 🏪 **8. Product Availability Monitor**
Alertas cuando productos agotados vuelven a stock (PS5, GPUs, etc.)

```python
# Monitorear:
# - Amazon, Best Buy, Newegg
# - Alerta cuando "Add to Cart" esté disponible
# - Auto-checkout (avanzado)
```

---

## 🎯 **CÓMO IMPLEMENTAR CUALQUIERA DE ESTOS**

### **Paso 1: Define tu objetivo**
```
"Necesito un monitor de precios para RTX 4090 en Amazon, Newegg, Best Buy"
```

### **Paso 2: Crea el Prompt Maestro**
```
Copia la plantilla de arriba y personaliza:
- Fuentes de datos (tiendas, job boards, etc.)
- Keywords y filtros
- Estructura de output (JSON, CSV, SQLite)
- Sistema de alertas (terminal, Discord, email)
```

### **Paso 3: Ejecuta Neo-Tokyo Dev**
```bash
echo "Monitor de precios" | python ai_duo.py "TU_PROMPT_MAESTRO"
```

### **Paso 4: El Dúo trabaja**
```
Arquitecto diseña (5-10 min)
Implementador codifica (5-10 min)
Artifact Extraction guarda el código
```

### **Paso 5: Ejecuta y disfruta**
```bash
python output/price_sentinel.py
# o
python output/job_hunter.py
```

---

## 🔮 **FILOSOFÍA DE ESCALAMIENTO**

```
╔══════════════════════════════════════════════════════════════════════╗
║  🚀 CUALQUIER CASO DE USO SIGUE EL MISMO PATRÓN:                     ║
╠══════════════════════════════════════════════════════════════════════╣
║  1. Define estructura de datos unificada                             ║
║  2. Async scraping con aiohttp + BeautifulSoup                       ║
║  3. Rate limiting + User-Agent rotation                              ║
║  4. Almacenamiento (JSON/CSV/SQLite)                                 ║
║  5. Sistema de alertas (logs/webhooks/email)                         ║
║  6. Logs neon cyberpunk                                              ║
║  7. Artifact Extraction automático                                   ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 💡 **PRO TIPS**

### **Para Web Scraping a Escala:**
1. **Respeta robots.txt** → Usa `robotparser` o biblioteca `reppy`
2. **Rate limiting agresivo** → Mínimo 1-2 segundos entre requests
3. **User-Agent rotation** → 5-10 agents diferentes
4. **Proxy rotation** (opcional) → Para evitar IP bans
5. **Headless browsers** (Selenium/Playwright) → Para sites con JS pesado
6. **API oficial primero** → Siempre prefiere API oficial si existe

### **Para Datos Estructurados:**
1. **SQLite** → Para historial y queries complejas
2. **CSV** → Para análisis en Excel/Python/R
3. **JSON** → Para integración con otras apps
4. **Pandas** → Para análisis de datos avanzado

### **Para Alertas:**
1. **Terminal** → Logs neon (rápido, visual)
2. **Discord webhook** → Alertas móviles (5 líneas de código)
3. **Telegram bot** → Similar a Discord, más privado
4. **Email** → SMTP para alertas profesionales
5. **Pushbullet** → Notificaciones móviles directas

---

## 🌟 **CONCLUSIÓN**

El **Neo-Tokyo Dev v3.0** con **Artifact Extraction** te permite crear cualquier scraper/monitor en minutos, no horas.

**El límite es tu imaginación.** 🔮⚡

---

**Generado por: Neo-Tokyo Dev v3.0 Golden Stack**  
**Architect (Llama 3.1 @ 0.85) + Implementer (Qwen 2.5 Coder @ 0.3)**

