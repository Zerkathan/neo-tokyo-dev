# 🤖 Guía: Refactorizar Metatron Bot con Neo-Tokyo Dev

## 🎯 **Dos Formas de Hacerlo**

---

## **FORMA 1: Usando el Script Helper (MÁS FÁCIL)**

### Paso 1: Prepara tu código
```bash
# Si tu código está en un archivo
# Asegúrate de saber la ruta (ej: C:\bots\metatron_bot.py)
```

### Paso 2: Ejecuta el helper
```bash
python refactor_my_code.py
```

### Paso 3: Sigue las instrucciones
```
1. Elige opción 1 (tengo el código en un archivo)
2. Ingresa la ruta: C:\path\to\metatron_bot.py
3. Ingresa el contexto: "Bot de Discord para moderación y utilidades"
4. ¡Espera 1-2 minutos!
```

---

## **FORMA 2: Directo con ai_duo.py (MÁS CONTROL)**

### Paso 1: Copia tu código
```bash
# Abre tu archivo metatron_bot.py
# Copia TODO el contenido (Ctrl+A, Ctrl+C)
```

### Paso 2: Construye el prompt
```bash
python ai_duo.py "AQUÍ VA EL PROMPT COMPLETO"
```

**Prompt recomendado:**

```
Tengo un bot de Discord llamado Metatron con el siguiente código:

[PEGA TODO TU CÓDIGO AQUÍ - Incluye todo: imports, funciones, clases, todo]

PROBLEMAS ACTUALES:
1. Todo está en un solo archivo (~500+ líneas)
2. Lógica de negocio mezclada con comandos de Discord
3. No hay separación de responsabilidades
4. Difícil de testear
5. Difícil de agregar nuevas features sin romper algo

TAREA DE REFACTORIZACIÓN:
Refactoriza este código aplicando Clean Architecture y mejores prácticas:

ARQUITECTURA:
- Domain Layer: Entidades del bot (User, Server, Command, etc.)
- Application Layer: Casos de uso (ModerarUsuario, AsignarRol, etc.)
- Infrastructure Layer: Discord API, base de datos, APIs externas
- Presentation Layer: Comandos de Discord (usando Cogs)

PATRONES:
- Repository Pattern para datos (UserRepository, ServerRepository)
- Command Pattern para comandos del bot
- Dependency Injection para servicios
- Strategy Pattern si hay múltiples comportamientos

REQUISITOS:
- Type Hints completos (Python 3.9+)
- Docstrings estilo Google en todo
- Separar en múltiples archivos modulares
- Tests unitarios con pytest
- Mantener compatibilidad con discord.py 2.0+
- Configuración mediante .env
- Logging estructurado
- Manejo de errores robusto

ESTRUCTURA DE ARCHIVOS DESEADA:
metatron_bot/
├── domain/           # Entidades
├── application/      # Casos de uso
├── infrastructure/   # Discord, DB, APIs
├── presentation/     # Cogs/Commands
├── tests/           # Tests unitarios
└── config/          # Configuración
```

### Paso 3: Contexto
Cuando te pida el contexto, escribe:
```
Bot de Discord para moderación, gestión de roles y comandos de utilidad
```

---

## **FORMA 3: Para Código Muy Grande (Archivo)**

Si tu código es muy grande (1000+ líneas), mejor hazlo así:

### Opción A: Guardar en archivo temporal
```bash
# 1. Copia tu código
# 2. Pégalo en un nuevo archivo: temp_code.txt
# 3. Usa PowerShell:

$codigo = Get-Content temp_code.txt -Raw
$prompt = "Refactoriza este código de bot: $codigo [... resto del prompt ...]"
echo "Bot de Discord" | python ai_duo.py $prompt
```

### Opción B: Dividir en módulos primero
```bash
# Si tu código es MUY grande (2000+ líneas), pide refactorización por partes:

# Primera pasada - Arquitectura general
python ai_duo.py "Analiza este código de bot y diseña una arquitectura 
Clean Architecture con 4 capas. No implementes aún, solo diseña la estructura."

# Segunda pasada - Implementar Domain
python ai_duo.py "Implementa la capa Domain con estas entidades: [lista]"

# Y así sucesivamente...
```

---

## **📋 Template de Prompt para Diferentes Tipos de Bots**

### 🎮 **Bot de Discord**
```
Contexto: Bot de Discord con discord.py 2.0

Mantén:
- Compatibilidad con discord.py 2.0+
- Usa Cogs para organizar comandos
- Slash commands (/) modernos
- Intents correctos
- Event handlers separados
```

### 💬 **Bot de Telegram**
```
Contexto: Bot de Telegram con python-telegram-bot

Mantén:
- Compatibilidad con python-telegram-bot 20+
- Usa Handlers para comandos
- ConversationHandler para flujos
- Async/await
- Callback queries organizados
```

### 🔀 **Bot Multi-Plataforma**
```
Contexto: Bot multi-plataforma (Discord + Telegram)

Separar:
- Core de lógica (independiente de plataforma)
- Adapters por plataforma (DiscordAdapter, TelegramAdapter)
- Interface común (BotCommand, BotMessage, BotUser)
- Configuración por plataforma
```

---

## **🎯 Ejemplo Real Completo**

```powershell
# Navegar a la carpeta
cd C:\Antigravitypro\twoais

# Ejecutar (con código inline)
python ai_duo.py "Tengo un bot de Discord llamado Metatron. Código:

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def ban(ctx, member: discord.Member):
    await member.ban()
    await ctx.send(f'{member} baneado!')

# ... más código aquí ...

Refactoriza aplicando Clean Architecture, SOLID, separa en capas (Domain, 
Application, Infrastructure, Presentation), usa Type Hints, Dependency 
Injection, crea tests. Mantén compatibilidad con discord.py."

# Cuando pida contexto, escribe:
# Bot de Discord para moderación de servidor con 500 usuarios
```

---

## **⚠️  Tips Importantes**

### ✅ **HACER:**
- ✅ Incluir TODO tu código (imports, funciones, clases, todo)
- ✅ Ser específico sobre qué hace tu bot
- ✅ Mencionar el framework (discord.py, python-telegram-bot, etc.)
- ✅ Listar problemas actuales
- ✅ Especificar arquitectura deseada (Clean Architecture)
- ✅ Pedir tests

### ❌ **NO HACER:**
- ❌ Prompt vago: "mejora mi código"
- ❌ Solo pegar código sin contexto
- ❌ No mencionar el framework/librerías
- ❌ Olvidar pedir tests
- ❌ No especificar Type Hints

---

## **🔥 Problemas Comunes y Soluciones**

### Problema 1: "El código es muy largo"
**Solución:** Usa el script helper `refactor_my_code.py` o divide en partes

### Problema 2: "El bot usa muchas APIs externas"
**Solución:** Menciona explícitamente en el prompt:
```
"El bot usa estas APIs externas: [lista]
Crea Adapters/Clients para cada una con interfaces limpias"
```

### Problema 3: "Tengo base de datos mezclada"
**Solución:** Especifica:
```
"Separa la lógica de base de datos en Repository Pattern.
Crea interfaces Repository y luego implementaciones 
(SQLRepository, MongoRepository, etc.)"
```

### Problema 4: "Muchos comandos (50+)"
**Solución:**
```
"Agrupa comandos por categoría en Cogs/Handlers separados:
- ModerationCog
- UtilityCog  
- FunCog
etc."
```

---

## **📊 Qué Esperar del Output**

El Golden Stack te dará:

### 🏛️ Del Arquitecto (Llama 3.1):
```
1. Análisis de problemas
2. Diseño de arquitectura en capas
3. Patrones recomendados
4. Estructura de archivos
5. Flujo de dependencias
6. Consideraciones de seguridad
```

### ⚡ Del Implementador (Qwen 2.5 Coder):
```
1. Código refactorizado completo
2. Type hints en todo
3. Docstrings exhaustivos
4. Múltiples archivos/módulos
5. Tests unitarios
6. Manejo de errores mejorado
7. Configuración separada
```

---

## **🚀 Después de la Refactorización**

### 1. Revisar el output
```bash
# El sistema imprimirá todo en la terminal
# Copia y pega en archivos separados según la estructura sugerida
```

### 2. Crear la estructura
```bash
mkdir -p metatron_bot/{domain,application,infrastructure,presentation,tests}
```

### 3. Implementar gradualmente
```bash
# No cambies todo de golpe
# Ve archivo por archivo
# Prueba cada módulo
```

### 4. Ejecutar tests
```bash
pytest tests/
```

---

## **💡 Casos de Uso Reales**

### Caso 1: Bot de Moderación con DB
```
"Refactoriza mi bot de moderación que usa SQLite. 
Separa comandos de Discord de la lógica de DB. 
Crea WarningRepository, UserRepository. 
Implementa casos de uso: AddWarning, CheckUserWarnings, BanUser."
```

### Caso 2: Bot con APIs Externas
```
"Mi bot consulta 3 APIs (OpenAI, Weather, News). 
Crea Adapters para cada API. 
Implementa Circuit Breaker para fallos. 
Separa la lógica del bot de las APIs."
```

### Caso 3: Bot con Economía Interna
```
"Bot con sistema de economía (monedas, tienda, inventory). 
Refactoriza separando: EconomyDomain (User, Item, Transaction), 
EconomyService (ComprarItem, TransferirMonedas), 
EconomyRepository para persistencia."
```

---

## **🎓 Recursos Adicionales**

- `REFACTORIZATION_SUMMARY.md` - Ver ejemplo de biblioteca
- `rate_limiter.py` - Ver ejemplo de código limpio
- `setup_golden_stack.md` - Instalación de Ollama
- `quick_start.md` - Guía rápida

---

**Generado por: Neo-Tokyo Dev v3.0**
🏛️ Arquitecto: Llama 3.1 | ⚡ Implementador: Qwen 2.5 Coder | 💰 Costo: $0.00

