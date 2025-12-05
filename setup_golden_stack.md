# 🏆 GOLDEN STACK SETUP - 100% GRATIS, NIVEL DIOS

## ¿Por qué esta combinación es superior?

```
╔════════════════════════════════════════════════════════════════╗
║  🏛️ ARQUITECTO: Llama 3.1 (8B)  │  ⚡ IMPLEMENTADOR: Qwen 2.5 Coder (7B)  ║
║  ✓ Razonamiento lógico          │  ✓ Supera a GPT-4 en código           ║
║  ✓ Planificación estratégica    │  ✓ Sintaxis perfecta                  ║
║  ✓ Contexto de negocio          │  ✓ Refactorización experta            ║
╚════════════════════════════════════════════════════════════════╝
```

### 🎯 Ventajas del Golden Stack

1. **Especialización**: No usas el mismo cerebro para todo
   - Llama 3.1 = El Gerente (entiende lógica humana y negocio)
   - Qwen Coder = El Ingeniero (entiende sintaxis y librerías)

2. **Velocidad**: Modelos pequeños (7B-8B parámetros)
   - Corren en laptops normales (16GB RAM)
   - No necesitas GPU gigante
   - Respuestas en segundos

3. **Costo**: **$0.00** - Cero API keys, cero límites

---

## 📦 PASO 1: Instalar Ollama

### Windows
1. Descarga Ollama desde: https://ollama.ai/download
2. Ejecuta el instalador
3. Verifica la instalación:
   ```powershell
   ollama --version
   ```

### macOS/Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

---

## 🚀 PASO 2: Descargar los Modelos

Abre tu terminal y ejecuta estos comandos:

### 1. Arquitecto Supremo (Llama 3.1)
```bash
ollama pull llama3.1
```

**Info del modelo:**
- Parámetros: 8B
- Tamaño: ~4.7 GB
- RAM necesaria: ~8 GB
- Especialidad: Razonamiento lógico y planificación

### 2. Implementador Supremo (Qwen 2.5 Coder)
```bash
ollama pull qwen2.5-coder
```

**Info del modelo:**
- Parámetros: 7B
- Tamaño: ~4.3 GB
- RAM necesaria: ~8 GB
- Especialidad: Código puro (supera GPT-4 en benchmarks)

### Verificar modelos instalados
```bash
ollama list
```

Deberías ver algo como:
```
NAME                ID              SIZE      MODIFIED
llama3.1:latest     abc123def       4.7 GB    2 minutes ago
qwen2.5-coder:latest xyz789ghi      4.3 GB    1 minute ago
```

---

## ⚙️ PASO 3: Configuración ya está lista

El archivo `.env` ya está configurado con:

```env
# 🏛️ ARQUITECTO → Llama 3.1
REVIEW_PROVIDER=ollama
REVIEW_MODEL=llama3.1

# ⚡ IMPLEMENTADOR → Qwen 2.5 Coder
DEV_PROVIDER=ollama
DEV_MODEL=qwen2.5-coder

# 🔌 Conexión local
LLAMA_BASE_URL=http://localhost:11434/v1
LLAMA_API_KEY=ollama
```

---

## 🧪 PASO 4: Probar el Sistema

```bash
# Test básico
python ai_duo.py "Crear una función de validación de emails con regex"

# Test intermedio
python ai_duo.py "Implementar un sistema de caché LRU con complejidad O(1)"

# Test avanzado
python ai_duo.py "Diseñar una API REST con autenticación JWT y rate limiting"
```

---

## 📊 Benchmarks - ¿Por qué Qwen 2.5 Coder?

### HumanEval (Benchmark de código Python)

| Modelo | Score | Notas |
|--------|-------|-------|
| **Qwen 2.5 Coder 7B** | **61.5%** | 🏆 Mejor en su categoría |
| GPT-4 (early) | 67.0% | Más caro, no es local |
| Llama 3.1 8B | 48.0% | Mejor en razonamiento general |
| CodeLlama 7B | 45.5% | Especializado pero inferior |
| Gemini 1.5 Flash | ~52%* | Requiere API key |

*Estimado basado en benchmarks públicos

### MBPP (More Basic Python Problems)

| Modelo | Score |
|--------|-------|
| **Qwen 2.5 Coder 7B** | **70.2%** |
| GPT-4 | 75.0% |
| Llama 3.1 8B | 55.0% |

**Conclusión**: Qwen 2.5 Coder a 7B está a solo 5-13 puntos de GPT-4, pero es:
- ✅ Gratis
- ✅ Local (privacidad total)
- ✅ Sin límites de rate

---

## 🔧 Troubleshooting

### Problema: "ollama: command not found"
**Solución**: 
- Windows: Reinicia la terminal después de instalar
- macOS/Linux: Ejecuta `source ~/.bashrc` o `source ~/.zshrc`

### Problema: "Connection refused at localhost:11434"
**Solución**: Ollama no está corriendo
```bash
# Windows (se inicia automáticamente, pero si no):
# Busca "Ollama" en el menú inicio y ábrelo

# macOS/Linux:
ollama serve
```

### Problema: Modelos muy lentos
**Posibles causas**:
1. RAM insuficiente (mínimo 16GB recomendado para ambos modelos)
2. Muchas aplicaciones abiertas
3. Modelo muy grande para tu hardware

**Soluciones**:
```bash
# Usa versiones cuantizadas (más rápidas, menos precisión):
ollama pull llama3.1:7b-instruct-q4_0
ollama pull qwen2.5-coder:7b-instruct-q4_0

# Actualiza el .env:
REVIEW_MODEL=llama3.1:7b-instruct-q4_0
DEV_MODEL=qwen2.5-coder:7b-instruct-q4_0
```

### Problema: Respuestas de baja calidad
**Nota**: Los modelos locales son muy buenos pero no mágicos. Para máxima calidad:
- Usa prompts más específicos
- Da más contexto en el problema
- Considera usar Claude/GPT-4 para proyectos críticos

---

## 💡 Tips Pro

### 1. Mix & Match según necesidad
```env
# Para proyectos simples: Todo local
REVIEW_PROVIDER=ollama
DEV_PROVIDER=ollama

# Para proyectos críticos: Arquitecto remoto, código local
REVIEW_PROVIDER=anthropic
REVIEW_MODEL=claude-sonnet-4-20250514
DEV_PROVIDER=ollama
DEV_MODEL=qwen2.5-coder
```

### 2. Monitorear uso de recursos
```bash
# Ver modelos cargados en memoria
ollama ps

# Si quieres liberar memoria
ollama stop llama3.1
ollama stop qwen2.5-coder
```

### 3. Actualizar modelos
```bash
# Los modelos se actualizan regularmente
ollama pull llama3.1  # actualiza si hay nueva versión
ollama pull qwen2.5-coder
```

---

## 🎓 Recursos Adicionales

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Qwen 2.5 Paper](https://arxiv.org/abs/2309.16609)
- [Llama 3.1 Blog Post](https://ai.meta.com/blog/meta-llama-3-1/)
- [HumanEval Benchmark](https://github.com/openai/human-eval)

---

## ✅ Checklist de Setup Completo

- [ ] Ollama instalado (`ollama --version`)
- [ ] Llama 3.1 descargado (`ollama list`)
- [ ] Qwen 2.5 Coder descargado (`ollama list`)
- [ ] Archivo `.env` configurado
- [ ] Ollama corriendo (`ollama ps`)
- [ ] Test ejecutado exitosamente

**¡Listo! Tienes un sistema de colaboración IA de nivel FAANG, completamente gratis.** 🔮⚡

