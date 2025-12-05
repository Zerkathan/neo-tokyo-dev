# ⚡ QUICK START - Neo-Tokyo Dev v3.0

## 🚀 De 0 a 100 en 5 minutos

### Para Usuarios que Quieren TODO GRATIS 🏆

```bash
# 1. Instalar Ollama
# Windows: Descargar de https://ollama.ai/download
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# 2. Descargar los 2 modelos del Golden Stack
ollama pull llama3.1
ollama pull qwen2.5-coder

# 3. Instalar dependencias Python
pip install -r requirements.txt

# 4. ¡Listo! El .env ya está configurado
python ai_duo.py "Crear una función de validación de emails"
```

**Tiempo total:** ~10 minutos (dependiendo de tu internet para descargar ~9GB)

---

### Para Usuarios con API Keys 💳

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Editar .env y agregar tu API key
# Para Gemini:
REVIEW_PROVIDER=gemini
REVIEW_MODEL=gemini-1.5-pro
DEV_PROVIDER=gemini
DEV_MODEL=gemini-1.5-flash
GOOGLE_API_KEY=tu-api-key-aqui

# 3. ¡Ejecutar!
python ai_duo.py "Tu problema aquí"
```

**Tiempo total:** 2 minutos

---

## 🧪 Primer Test

```bash
# Test simple
python ai_duo.py "Crear una función que calcule el factorial de un número"

# Ver ejemplos más complejos
python test_example.py
```

---

## 📊 ¿Qué Stack Usar?

| Stack | Costo | Velocidad | Calidad | Mejor Para |
|-------|-------|-----------|---------|------------|
| 🏆 **Golden Stack**<br>(Llama 3.1 + Qwen) | **$0** | ⚡⚡⚡ | ⭐⭐⭐⭐ | Aprendizaje, proyectos personales |
| 💎 **Claude Sonnet** | $$$ | ⚡⚡ | ⭐⭐⭐⭐⭐ | Producción crítica |
| ⚡ **Gemini Flash** | $ | ⚡⚡⚡⚡ | ⭐⭐⭐ | Iteración rápida |
| 🎯 **Híbrido**<br>(Qwen + Claude) | $$ | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Óptimo precio/calidad |

---

## ❓ FAQ Rápido

### ¿Necesito GPU?
**No.** Los modelos del Golden Stack corren en CPU con 16GB RAM.

### ¿Puedo mezclar local y cloud?
**Sí.** Usa Qwen local para código y Claude para arquitectura:
```env
DEV_PROVIDER=ollama
DEV_MODEL=qwen2.5-coder
REVIEW_PROVIDER=anthropic
REVIEW_MODEL=claude-sonnet-4-20250514
```

### ¿Qué tan bueno es Qwen vs GPT-4?
En **código puro**, Qwen 2.5 Coder (7B) está a ~5-10% de GPT-4, pero es:
- ✅ Gratis
- ✅ Local (privacidad)
- ✅ Sin rate limits

### Ollama no arranca
```bash
# Windows: Busca "Ollama" en el menú inicio
# macOS/Linux:
ollama serve
```

---

## 🎓 Próximos Pasos

1. ✅ **Completar setup** (arriba)
2. 📖 **Leer** [setup_golden_stack.md](setup_golden_stack.md) para detalles
3. 🧪 **Probar** con `test_example.py`
4. 🚀 **Usar** en tus proyectos reales

---

**¿Problemas?** Abre un issue o consulta la [documentación completa](README.md).

