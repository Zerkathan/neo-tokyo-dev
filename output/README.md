# 💾 Output Directory - Artifact Extraction

## 🎯 **Qué es Esta Carpeta**

Cuando ejecutas Neo-Tokyo Dev, el **Protocolo "Artifact Extraction"** guarda automáticamente todo el código generado aquí.

```bash
python ai_duo.py "Crea una API REST"

# El sistema automáticamente guarda:
output/artifact_20251205_143022_1.py  ← Tu código aquí
output/artifact_20251205_143022_2.py  ← Más código si hay
```

---

## 📋 **Naming Convention**

```
artifact_YYYYMMDD_HHMMSS_N.extension

Donde:
• YYYYMMDD: Fecha (año, mes, día)
• HHMMSS: Hora (hora, minuto, segundo)
• N: Número secuencial (si hay múltiples bloques)
• extension: .py, .js, .ts, .go, .rs, etc.
```

**Ejemplos:**
```
artifact_20251205_143022_1.py   → Primer bloque Python
artifact_20251205_143022_2.js   → Segundo bloque JavaScript
artifact_20251205_150315_1.go   → Bloque Go (otra ejecución)
```

---

## 🚀 **Uso Típico**

```bash
# 1. Generar código
python ai_duo.py "Crea un web scraper con BeautifulSoup"

# 2. Ver el log
[02:20:41.176] ▸ INFO  💾 Artifact saved: artifact_20251205_022041_1.py (2341 chars, python)
[02:20:41.176] ▸ INFO  ✅ 1 artifact(s) secured in: output/

# 3. Usar el código
cd output/
python artifact_20251205_022041_1.py
# ¡Funciona!
```

---

## 📦 **Lenguajes Soportados**

El sistema detecta automáticamente la extensión:

```
Python       → .py
JavaScript   → .js
TypeScript   → .ts
Java         → .java
C++          → .cpp
C            → .c
Go           → .go
Rust         → .rs
Ruby         → .rb
PHP          → .php
Bash         → .sh
SQL          → .sql
YAML         → .yaml
HTML         → .html
CSS          → .css
```

---

## 🔧 **Características**

### **Extracción Inteligente:**
- ✅ Detecta bloques de código en markdown (```language)
- ✅ Filtra JSON (no es código ejecutable)
- ✅ Filtra snippets muy pequeños (<20 chars)
- ✅ Maneja múltiples bloques en una respuesta

### **Guardado Robusto:**
- ✅ Crea la carpeta si no existe
- ✅ Nombres únicos (timestamp + secuencial)
- ✅ UTF-8 encoding
- ✅ Manejo de errores I/O (no crashea)

### **Logging Integrado:**
- ✅ Muestra qué se guardó
- ✅ Muestra tamaño y lenguaje
- ✅ Estilo cyberpunk
- ✅ Confirmación clara

---

## 💡 **Tips**

### **Organizar Outputs:**
```bash
# Crear subcarpetas por proyecto
mkdir output/mi_proyecto
# Mover archivos relevantes
mv output/artifact_*.py output/mi_proyecto/
```

### **Renombrar Archivos:**
```bash
# Darles nombres descriptivos
mv output/artifact_20251205_143022_1.py output/api_rest.py
mv output/artifact_20251205_143022_2.py output/models.py
```

### **Limpiar Old Artifacts:**
```bash
# Limpiar archivos viejos (cuidado!)
rm output/artifact_2025110*  # Noviembre
```

---

## 📊 **Estadísticas de Uso**

Cada vez que ejecutes Neo-Tokyo Dev y genere código:
- ✅ Código guardado automáticamente
- ✅ No más copy-paste manual
- ✅ Timestamped para historial
- ✅ Listo para ejecutar
- ✅ Listo para modificar
- ✅ Listo para integrar en tu proyecto

---

## 🎓 **Ejemplo Completo**

```bash
# Sesión de generación de API
$ python ai_duo.py "Crea una API REST con FastAPI para gestión de usuarios"

# El sistema genera y guarda:
[System] 💾 Artifact saved: artifact_20251205_150000_1.py (1245 chars, python)
[System] 💾 Artifact saved: artifact_20251205_150000_2.py (856 chars, python)
[System] 💾 Artifact saved: artifact_20251205_150000_3.py (432 chars, python)
[System] ✅ 3 artifact(s) secured in: output/

# Estructura generada:
output/
├── artifact_20251205_150000_1.py  # Main API
├── artifact_20251205_150000_2.py  # Models  
└── artifact_20251205_150000_3.py  # Tests

# Renombrar para tu proyecto:
$ cd output/
$ mv artifact_20251205_150000_1.py main.py
$ mv artifact_20251205_150000_2.py models.py
$ mv artifact_20251205_150000_3.py test_api.py

# ¡Listo para usar!
$ python main.py
```

---

## 🔮 **Powered by Artifact Extraction Protocol**

Implementado en: `ai_duo.py` (líneas 684-823)  
Activado por defecto: Sí ✅  
Configurable: Sí (output_dir puede cambiar)  
Costo: $0.00  
Valor: Incalculable (ahorra horas de copy-paste)  

---

**💾 Nunca más pierdas código generado por IA 💾**

**Generado por: Neo-Tokyo Dev v3.0 Golden Stack**

