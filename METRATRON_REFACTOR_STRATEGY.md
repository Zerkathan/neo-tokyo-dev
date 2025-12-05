# 🎬 Estrategia de Refactorización para Metratron Bot

## ⚠️ **Problema: Archivo Demasiado Grande**

Tu `dashboard.py` tiene **3,108 líneas** - es demasiado para refactorizar de una vez. 

**Solución:** Refactorización **incremental** por fases.

---

## 📋 **FASE 1: Análisis y Arquitectura (AHORA)**

### Ejecuta Esto Para Obtener el Diseño Arquitectónico:

```bash
python ai_duo.py "Tengo un automatizador de videos para YouTube/TikTok con 3,108 líneas en un archivo. Incluye: Streamlit UI, generación de videos con MoviePy, subida a plataformas, 12 estilos de video, scheduling automático. NO implementes código aún, solo DISEÑA la arquitectura Clean Architecture ideal: estructura de carpetas, capas (Domain, Application, Infrastructure, Presentation), patrones a aplicar (Repository, Factory, Strategy), y plan de migración incremental."
```

**Contexto:** `Sistema de automatización de videos para YouTube/TikTok/Instagram`

---

## 🏗️ **FASE 2: Refactorización Por Módulos**

Divide en partes pequeñas:

### **2.1 - Extraer Estilos de Video**

```bash
python ai_duo.py "Extrae la lógica de estilos de video de este código: [PEGA SOLO LA PARTE DE STYLES]. Crea: 1) domain/entities/style.py con clase Style 2) domain/value_objects/style_config.py 3) application/factories/style_factory.py con Factory Pattern. Type hints completos."
```

### **2.2 - Extraer Uploaders**

```bash
python ai_duo.py "Extrae la lógica de subida a plataformas: [PEGA CÓDIGO DE UPLOADERS]. Crea: 1) application/interfaces/platform_uploader.py (ABC) 2) infrastructure/uploaders/youtube_uploader.py 3) infrastructure/uploaders/tiktok_uploader.py 4) infrastructure/uploaders/instagram_uploader.py. Strategy Pattern con DI."
```

### **2.3 - Extraer Generador de Videos**

```bash
python ai_duo.py "Extrae la lógica de generación de videos: [PEGA FUNCIÓN PRINCIPAL]. Crea: 1) application/use_cases/generate_video.py 2) application/services/video_generator.py 3) infrastructure/video_editing/moviepy_editor.py. Async, Type hints, tests."
```

### **2.4 - Extraer Scheduler**

```bash
python ai_duo.py "Extrae la lógica de scheduling: [PEGA CÓDIGO DE BUCLE]. Crea: 1) application/use_cases/schedule_generation.py 2) domain/value_objects/schedule.py 3) application/services/scheduler.py con manejo de horarios y modo sueño."
```

### **2.5 - Extraer UI de Streamlit**

```bash
python ai_duo.py "Refactoriza la UI de Streamlit separándola de lógica: [PEGA CÓDIGO DE UI]. Crea: presentation/streamlit_app/dashboard.py (solo UI), components/video_generator_ui.py, components/gallery_ui.py, state_manager.py. UI solo llama a Use Cases."
```

---

## 🎯 **FASE 3: Plan de Migración Incremental**

### Paso 1: Crear Estructura Base
```bash
mkdir metratron_refactored
cd metratron_refactored
mkdir -p domain/{entities,value_objects}
mkdir -p application/{use_cases,services,interfaces,factories}
mkdir -p infrastructure/{video_editing,uploaders,external_apis,storage}
mkdir -p presentation/{streamlit_app/components}
mkdir -p tests/{unit,integration}
```

### Paso 2: Migrar Módulo por Módulo
```
1. Migrar Estilos (más simple)
   - Crear style.py, style_factory.py
   - Actualizar imports en dashboard.py
   - Probar que sigue funcionando

2. Migrar Uploaders
   - Crear uploaders separados
   - Actualizar imports
   - Probar uploads

3. Migrar Generador
   - Extraer lógica de generación
   - Mantener compatibilidad
   - Probar generación end-to-end

4. Migrar Scheduler
   - Extraer bucle automático
   - Probar scheduling

5. Refactorizar UI (último)
   - Separar componentes
   - Conectar con Use Cases
```

### Paso 3: Ejecutar Ambos en Paralelo
```bash
# Mantén el dashboard.py original funcionando
python dashboard.py  # Puerto 8501

# Mientras desarrollas el refactorizado
cd metratron_refactored
python presentation/streamlit_app/dashboard.py  # Puerto 8502
```

---

## 📝 **Arquitectura Objetivo**

```
metratron_refactored/
├── domain/                      # REGLAS DE NEGOCIO
│   ├── entities/
│   │   ├── video.py            # Video, VideoConfig
│   │   ├── style.py            # Style (Horror, Motivación, etc.)
│   │   ├── profile.py          # Profile, ProfileSettings
│   │   └── upload.py           # Upload, UploadResult
│   └── value_objects/
│       ├── video_format.py     # Resolution, Duration, AspectRatio
│       └── schedule.py         # Schedule, TimeWindow
│
├── application/                 # CASOS DE USO
│   ├── use_cases/
│   │   ├── generate_video.py
│   │   ├── upload_video.py
│   │   ├── schedule_generation.py
│   │   └── manage_profiles.py
│   ├── services/
│   │   ├── video_generator.py  # Orquesta generación completa
│   │   ├── content_creator.py  # Guiones con LLM
│   │   └── scheduler.py        # Scheduling automático
│   ├── interfaces/              # ABC/Protocols
│   │   ├── video_editor.py
│   │   ├── platform_uploader.py
│   │   └── content_repository.py
│   └── factories/
│       └── style_factory.py    # Factory para estilos
│
├── infrastructure/              # DETALLES TÉCNICOS
│   ├── video_editing/
│   │   ├── moviepy_editor.py   # Implementación MoviePy
│   │   └── effects/            # Efectos por estilo
│   ├── uploaders/
│   │   ├── youtube_uploader.py
│   │   ├── tiktok_uploader.py
│   │   └── instagram_uploader.py
│   ├── external_apis/
│   │   ├── llm_client.py
│   │   ├── tts_client.py
│   │   └── media_provider.py
│   └── storage/
│       ├── file_storage.py
│       └── video_repository.py
│
├── presentation/                # UI/INTERFACES
│   └── streamlit_app/
│       ├── dashboard.py        # Main (limpio, solo UI)
│       ├── components/
│       │   ├── generator_ui.py
│       │   ├── gallery_ui.py
│       │   ├── analytics_ui.py
│       │   └── settings_ui.py
│       └── state_manager.py
│
├── tests/
│   ├── unit/
│   │   ├── test_style_factory.py
│   │   ├── test_uploaders.py
│   │   └── test_video_generator.py
│   └── integration/
│       └── test_full_pipeline.py
│
└── config/
    ├── settings.py             # Configuración
    └── .env                    # Variables de entorno
```

---

## 🚀 **Comando Rápido Para Empezar**

### Obtener Arquitectura Completa:
```bash
python ai_duo.py "Soy desarrollador con un automatizador de videos de 3,108 líneas (Streamlit + MoviePy + YouTube/TikTok uploads). Diseña SOLO la arquitectura Clean Architecture completa: estructura de carpetas detallada, qué va en cada capa (Domain, Application, Infrastructure, Presentation), qué patrones usar (Repository, Factory, Strategy, DI), y plan de migración incremental desde el monolito. NO escribas código aún."
```

**Contexto:** `Automatizador de videos YouTube/TikTok con Streamlit`

---

## 💡 **Tips Para la Refactorización**

### ✅ **HACER:**
1. ✅ Refactorizar módulo por módulo
2. ✅ Mantener el original funcionando
3. ✅ Probar cada módulo antes de continuar
4. ✅ Usar Git para control de versiones
5. ✅ Escribir tests para nuevos módulos

### ❌ **NO HACER:**
1. ❌ Intentar refactorizar todo de golpe
2. ❌ Borrar el dashboard.py original
3. ❌ Cambiar sin probar
4. ❌ Olvidar los tests
5. ❌ Mezclar refactorización con nuevas features

---

## 🎯 **Orden Recomendado de Refactorización**

```
SEMANA 1: Fundamentos
├─ Día 1-2: Arquitectura y estructura de carpetas
├─ Día 3-4: Domain (Entities + Value Objects)
└─ Día 5-7: Tests para Domain

SEMANA 2: Application Layer
├─ Día 1-2: Interfaces (ABC/Protocols)
├─ Día 3-4: Factories (StyleFactory)
├─ Día 5-6: Services (VideoGenerator, ContentCreator)
└─ Día 7: Tests para Services

SEMANA 3: Infrastructure
├─ Día 1-2: VideoEditor (MoviePy wrapper)
├─ Día 3-4: Uploaders (YouTube, TikTok, IG)
├─ Día 5-6: External APIs (LLM, TTS)
└─ Día 7: Tests para Infrastructure

SEMANA 4: Use Cases + Presentation
├─ Día 1-3: Use Cases (GenerateVideo, UploadVideo, etc.)
├─ Día 4-6: Streamlit UI refactorizada
└─ Día 7: Tests de integración

SEMANA 5: Migración y Pruebas
├─ Día 1-3: Migración gradual desde dashboard.py
├─ Día 4-5: Pruebas end-to-end
└─ Día 6-7: Deploy y monitoring
```

---

## 🔧 **Herramientas de Apoyo**

### Script para Extraer Secciones:
```python
# extract_section.py
import sys

def extract_section(file_path, start_line, end_line):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return ''.join(lines[start_line-1:end_line])

if __name__ == "__main__":
    section = extract_section(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    print(section)
```

**Uso:**
```bash
# Extraer líneas 100-200 para refactorizar
python extract_section.py C:\Metratron_bot\dashboard.py 100 200 > section_to_refactor.py

# Refactorizar solo esa sección
python ai_duo.py "Refactoriza este código: $(cat section_to_refactor.py)"
```

---

## 📚 **Recursos Adicionales**

- `REFACTORIZATION_SUMMARY.md` - Ejemplo de biblioteca refactorizada
- `rate_limiter.py` - Ejemplo de Clean Architecture simple
- `METATRON_REFACTOR_GUIDE.md` - Guía completa

---

## ✅ **Checklist de Refactorización**

```
PREPARACIÓN:
[ ] Backup del código original
[ ] Configurar Git con .gitignore
[ ] Crear requirements.txt con todas las dependencias
[ ] Documentar funcionalidad actual

DOMAIN:
[ ] Crear entities (Video, Style, Profile, Upload)
[ ] Crear value objects (VideoFormat, Schedule)
[ ] Tests para entities

APPLICATION:
[ ] Crear interfaces (ABC/Protocols)
[ ] Crear factories (StyleFactory)
[ ] Crear services (VideoGenerator, etc.)
[ ] Crear use cases (GenerateVideo, etc.)
[ ] Tests para services y use cases

INFRASTRUCTURE:
[ ] Implementar VideoEditor (MoviePy)
[ ] Implementar Uploaders (YouTube, TikTok, IG)
[ ] Implementar External APIs (LLM, TTS)
[ ] Implementar Storage/Repository
[ ] Tests para infrastructure

PRESENTATION:
[ ] Refactorizar Streamlit UI
[ ] Separar en components
[ ] State management limpio
[ ] Tests para UI (selenium/playwright)

MIGRACIÓN:
[ ] Funcionalidad completa en nuevo código
[ ] Tests end-to-end pasando
[ ] Performance igual o mejor
[ ] Documentación actualizada
[ ] Deploy exitoso
```

---

**💪 TÚ PUEDES HACERLO. Paso a paso, módulo a módulo.**

¿Quieres empezar con la arquitectura general o prefieres refactorizar un módulo específico primero?

