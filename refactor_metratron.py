#!/usr/bin/env python3
"""
🎬 Refactorización Específica para Metratron Bot
"""

import subprocess
import sys
from pathlib import Path

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🎬 REFACTORIZACIÓN - METRATRON BOT                                          ║
║  Automatizador de Videos para YouTube/TikTok/Instagram                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

# Leer el código
dashboard_path = Path(r"C:\Metratron_bot\dashboard.py")

if not dashboard_path.exists():
    print(f"❌ Error: No se encontró {dashboard_path}")
    print("   Verifica la ruta del archivo")
    sys.exit(1)

print(f"📄 Leyendo código de: {dashboard_path}")
with open(dashboard_path, 'r', encoding='utf-8') as f:
    codigo = f.read()

print(f"✅ Código cargado: {len(codigo):,} caracteres, ~{len(codigo.splitlines())} líneas")

# Prompt específico para Metratron
prompt = f"""Tengo un sistema de automatización de videos para YouTube/TikTok/Instagram llamado METRATRON.

CÓDIGO ACTUAL (3,108 líneas en UN archivo - ESPAGUETI TOTAL):
{codigo}

DESCRIPCIÓN DEL SISTEMA:
- Interfaz Streamlit (dashboard web)
- Genera videos cortos automáticamente
- 12 estilos diferentes (Horror, Motivación, Curiosidades, etc.)
- Sube a YouTube, TikTok e Instagram
- Scheduling automático con horarios
- Usa MoviePy para edición de video
- Integra APIs (LLM para guiones, TTS para voz)
- Analytics y gestión de perfiles
- Limpieza automática de disco

PROBLEMAS ACTUALES:
1. TODO en un archivo gigante (3,108 líneas)
2. UI de Streamlit mezclada con lógica de negocio
3. Sin separación de responsabilidades
4. Imposible de testear
5. Difícil agregar nuevas features
6. Difícil agregar nuevas plataformas (YouTube, TikTok, etc.)
7. Configuración hardcodeada
8. Sin manejo robusto de errores

TAREA DE REFACTORIZACIÓN:
Refactoriza COMPLETAMENTE aplicando Clean Architecture profesional.

ARQUITECTURA OBJETIVO:

📦 metratron/
├── domain/                    # CAPA DE DOMINIO
│   ├── entities/
│   │   ├── video.py          # Video, VideoConfig, VideoMetadata
│   │   ├── profile.py        # Profile, ProfileSettings
│   │   ├── style.py          # Style, StyleConfig (Horror, Motivación, etc.)
│   │   ├── upload.py         # Upload, UploadResult, Platform
│   │   └── analytics.py      # Analytics, GenerationStats
│   └── value_objects/
│       ├── video_format.py   # Resolution, AspectRatio, Duration
│       └── schedule.py       # Schedule, TimeWindow
│
├── application/               # CAPA DE APLICACIÓN (Casos de Uso)
│   ├── use_cases/
│   │   ├── generate_video.py      # GenerateVideoUseCase
│   │   ├── upload_video.py        # UploadVideoUseCase
│   │   ├── schedule_generation.py # ScheduleGenerationUseCase
│   │   ├── manage_profiles.py     # ManageProfilesUseCase
│   │   └── analyze_performance.py # AnalyzePerformanceUseCase
│   ├── services/
│   │   ├── video_generator.py    # Orquesta generación completa
│   │   ├── content_creator.py    # Crea guiones/scripts
│   │   └── scheduler.py          # Maneja scheduling automático
│   └── interfaces/                # Interfaces (Abstract)
│       ├── video_editor.py
│       ├── platform_uploader.py
│       ├── content_repository.py
│       └── analytics_repository.py
│
├── infrastructure/            # CAPA DE INFRAESTRUCTURA
│   ├── video_editing/
│   │   ├── moviepy_editor.py     # Implementación con MoviePy
│   │   └── effects/              # Efectos visuales por estilo
│   ├── platform_uploaders/
│   │   ├── youtube_uploader.py   # Cliente YouTube API
│   │   ├── tiktok_uploader.py    # Cliente TikTok
│   │   └── instagram_uploader.py # Cliente Instagram
│   ├── external_apis/
│   │   ├── llm_client.py         # Cliente para LLM (guiones)
│   │   ├── tts_client.py         # Cliente TTS (voz)
│   │   └── media_provider.py     # Pexels, Unsplash, etc.
│   ├── storage/
│   │   ├── file_storage.py       # Sistema de archivos
│   │   └── database.py           # SQLite/JSON para metadata
│   └── config/
│       └── settings.py           # Carga .env, configuración
│
├── presentation/              # CAPA DE PRESENTACIÓN
│   ├── streamlit_app/
│   │   ├── dashboard.py          # Main Streamlit UI (LIMPIO)
│   │   ├── components/           # Componentes reutilizables
│   │   │   ├── video_generator_ui.py
│   │   │   ├── gallery_ui.py
│   │   │   ├── analytics_ui.py
│   │   │   └── settings_ui.py
│   │   └── state_manager.py      # Gestión de estado Streamlit
│   └── cli/                      # (Opcional) CLI
│       └── commands.py
│
└── tests/                     # TESTS
    ├── unit/
    │   ├── test_video_generator.py
    │   ├── test_uploaders.py
    │   └── test_use_cases.py
    └── integration/
        └── test_full_pipeline.py

PATRONES A APLICAR:
1. Repository Pattern: Para acceso a datos (videos, profiles, analytics)
2. Factory Pattern: Para crear estilos de video (StyleFactory)
3. Strategy Pattern: Para diferentes plataformas de upload
4. Command Pattern: Para operaciones async (GenerateCommand, UploadCommand)
5. Dependency Injection: Inyectar servicios en casos de uso
6. Observer Pattern: Para notificaciones de progreso

REQUISITOS TÉCNICOS:
- Type Hints COMPLETOS (Python 3.10+)
- Docstrings estilo Google en TODAS las clases y funciones
- Async/await donde sea posible (uploads, API calls)
- Manejo robusto de errores con excepciones custom
- Logging estructurado (loguru)
- Configuración externa (.env + config.yaml)
- Tests unitarios con pytest
- Tests de integración para pipeline completo

REQUISITOS FUNCIONALES:
- Mantener TODA la funcionalidad actual
- Mantener compatibilidad con Streamlit
- Mantener compatibilidad con MoviePy
- Los 12 estilos deben seguir funcionando
- El scheduling automático debe seguir funcionando
- Las subidas a plataformas deben seguir funcionando

RESULTADO ESPERADO:
Un sistema modular, mantenible, testeable y escalable donde:
- Es FÁCIL agregar nuevas plataformas (YouTube, TikTok, Discord, Twitter)
- Es FÁCIL agregar nuevos estilos de video
- Es FÁCIL testear cada componente
- El dashboard de Streamlit es SOLO UI, sin lógica
- La lógica de negocio está en Application layer
- Los detalles técnicos están en Infrastructure
- El dominio es independiente de todo

Por favor, proporciona:
1. La arquitectura completa explicada
2. El código de los archivos principales
3. Ejemplos de uso de los casos de uso
4. Cómo migrar del código actual al nuevo
"""

contexto = "Sistema de automatización de videos para YouTube/TikTok/Instagram con Streamlit"

print("\n" + "═" * 80)
print("🚀 INICIANDO REFACTORIZACIÓN CON GOLDEN STACK")
print("═" * 80)
print(f"\n⚠️  ADVERTENCIA: Este código es muy grande (3,108 líneas)")
print(f"⏳ La refactorización tomará 3-5 minutos")
print(f"💡 El Golden Stack iterará varias veces para diseñar todo")
print("\n" + "═" * 80 + "\n")

try:
    proceso = subprocess.Popen(
        ["python", "ai_duo.py", prompt],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8'
    )
    
    # Enviar contexto
    salida, _ = proceso.communicate(input=contexto + "\n", timeout=600)  # 10 min timeout
    
    print(salida)
    
    if proceso.returncode == 0:
        print("\n" + "═" * 80)
        print("✅ REFACTORIZACIÓN COMPLETADA")
        print("═" * 80)
        print("\n📋 PRÓXIMOS PASOS:")
        print("   1. Revisa la arquitectura propuesta arriba")
        print("   2. Crea la estructura de carpetas")
        print("   3. Implementa gradualmente, módulo por módulo")
        print("   4. Ejecuta tests para cada módulo")
        print("   5. Migra el dashboard.py poco a poco")
    else:
        print("\n❌ Error en la refactorización")
        
except subprocess.TimeoutExpired:
    print("\n⚠️  Timeout - El código es muy grande")
    print("   Considera dividir la refactorización en partes")
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)

