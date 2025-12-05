#!/usr/bin/env python3
"""
🔮 NEO-TOKYO DEV - Refactorizador de Código Propio
Script helper para refactorizar cualquier código con el Golden Stack
"""

import subprocess
import sys
from pathlib import Path

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔥 REFACTORIZADOR DE CÓDIGO - Neo-Tokyo Dev v3.0                            ║
║                                                                              ║
║  Este script te ayudará a refactorizar tu código usando el Golden Stack     ║
║  (Llama 3.1 + Qwen 2.5 Coder) completamente GRATIS                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

# Opciones
print("\n📋 ¿Cómo quieres proporcionar tu código?\n")
print("1. Tengo el código en un archivo")
print("2. Voy a pegar el código aquí")
print("3. Dame un ejemplo de prompt")

opcion = input("\n▸ Opción (1/2/3): ").strip()

if opcion == "1":
    # Leer desde archivo
    archivo = input("\n📄 Ruta del archivo (ej: metatron_bot.py): ").strip()
    
    if not Path(archivo).exists():
        print(f"\n❌ Error: El archivo '{archivo}' no existe")
        sys.exit(1)
    
    with open(archivo, 'r', encoding='utf-8') as f:
        codigo = f.read()
    
    print(f"\n✅ Código cargado: {len(codigo)} caracteres")
    
elif opcion == "2":
    # Pegar código
    print("\n📝 Pega tu código aquí (Ctrl+Z + Enter en Windows, Ctrl+D en Unix para terminar):")
    print("─" * 60)
    
    lineas = []
    try:
        while True:
            linea = input()
            lineas.append(linea)
    except EOFError:
        pass
    
    codigo = "\n".join(lineas)
    print(f"\n✅ Código capturado: {len(codigo)} caracteres")

elif opcion == "3":
    # Ejemplo de prompt
    print("""
═══════════════════════════════════════════════════════════════════════════════
📖 EJEMPLO DE PROMPT PARA REFACTORIZAR TU CÓDIGO
═══════════════════════════════════════════════════════════════════════════════

Para refactorizar tu Metatron Bot u otro código, usa este formato:

╔═══════════════════════════════════════════════════════════════════════════╗
║  PASO 1: Ejecuta el sistema                                              ║
╚═══════════════════════════════════════════════════════════════════════════╝

python ai_duo.py "PEGA TU PROMPT AQUÍ"

Cuando te pida el contexto, escribe algo como:
"Bot de Discord/Telegram para [describe qué hace]"


╔═══════════════════════════════════════════════════════════════════════════╗
║  PASO 2: Usa este prompt (copia y adapta)                                ║
╚═══════════════════════════════════════════════════════════════════════════╝

Tengo un bot llamado Metatron con el siguiente código:

[PEGA TODO TU CÓDIGO AQUÍ]

Este código funciona pero tiene problemas:
1. Todo está en un solo archivo
2. Lógica mezclada con comandos
3. Sin separación de responsabilidades
4. Difícil de testear
5. Difícil de extender con nuevas funcionalidades

TAREA: Refactorízalo completamente aplicando:
- Clean Architecture (Domain, Application, Infrastructure, Presentation)
- Principios SOLID
- Dependency Injection
- Repository Pattern para datos
- Command Pattern para los comandos del bot
- Type Hints completos
- Docstrings
- Tests unitarios
- Modularidad (separa en múltiples archivos)


╔═══════════════════════════════════════════════════════════════════════════╗
║  PASO 3: Para Metatron Bot específicamente                               ║
╚═══════════════════════════════════════════════════════════════════════════╝

Si tu bot es de Discord, agrega:
"Mantén la compatibilidad con discord.py, pero separa la lógica de negocio 
del framework. Implementa cogs/extensions para organizar comandos."

Si es de Telegram, agrega:
"Mantén la compatibilidad con python-telegram-bot, pero separa handlers 
de la lógica de negocio. Implementa un sistema de comandos modular."


╔═══════════════════════════════════════════════════════════════════════════╗
║  EJEMPLO COMPLETO                                                         ║
╚═══════════════════════════════════════════════════════════════════════════╝

python ai_duo.py "Tengo un bot de Discord llamado Metatron con 500 líneas 
de código en un solo archivo. Refactorízalo aplicando Clean Architecture: 
separa Domain (entidades), Application (casos de uso), Infrastructure 
(Discord API, base de datos), y Presentation (comandos). Usa SOLID, 
Dependency Injection, Type Hints y crea tests. Mantén compatibilidad 
con discord.py pero hazlo modular y testeable."

Contexto: "Bot de Discord para moderación y gestión de comunidad"


═══════════════════════════════════════════════════════════════════════════════
💡 TIPS IMPORTANTES
═══════════════════════════════════════════════════════════════════════════════

1. ✅ Sé específico sobre qué hace tu bot
2. ✅ Menciona los problemas actuales
3. ✅ Lista las tecnologías que usas (discord.py, telegram, etc.)
4. ✅ Di qué arquitectura/patrones quieres aplicar
5. ✅ Menciona si quieres tests

❌ NO hagas prompts muy vagos como "mejora este código"
✅ SÍ sé específico: "aplica Clean Architecture, separa en capas, etc."


═══════════════════════════════════════════════════════════════════════════════
🎯 ALTERNATIVA RÁPIDA: Usa este script
═══════════════════════════════════════════════════════════════════════════════

1. Guarda tu código en un archivo: metatron_bot.py
2. Ejecuta: python refactor_my_code.py
3. Elige opción 1
4. Ingresa la ruta del archivo
5. Deja que el Golden Stack haga su magia

""")
    sys.exit(0)

else:
    print("\n❌ Opción inválida")
    sys.exit(1)

# Contexto del proyecto
print("\n🌐 Contexto del proyecto:")
print("   Ejemplos: 'Bot de Discord para moderación'")
print("             'Bot de Telegram para crypto'")
print("             'Bot multi-plataforma de IA'")

contexto = input("\n▸ Contexto: ").strip()
if not contexto:
    contexto = "Bot de mensajería con funcionalidades avanzadas"

# Construir el prompt
prompt = f"""Tengo este código de un bot que funciona pero necesita refactorización completa:

CÓDIGO A REFACTORIZAR:
{codigo}

PROBLEMAS ACTUALES:
1. Todo en un solo archivo o función
2. Lógica mezclada con comandos/handlers
3. Sin separación de responsabilidades
4. Difícil de testear y mantener
5. Sin arquitectura clara

REQUISITOS DE REFACTORIZACIÓN:
1. Aplicar Clean Architecture (Domain, Application, Infrastructure, Presentation)
2. Principios SOLID (cada clase una responsabilidad)
3. Dependency Injection (inyectar dependencias)
4. Repository Pattern para persistencia de datos
5. Command/Handler Pattern para comandos del bot
6. Type Hints completos en todas las funciones
7. Docstrings exhaustivos estilo Google
8. Separar en múltiples archivos modulares
9. Tests unitarios con casos edge
10. Mantener compatibilidad con el framework actual del bot

OBJETIVO: Convertirlo en código production-ready, mantenible y escalable.
"""

print("\n" + "═" * 80)
print("🚀 INICIANDO REFACTORIZACIÓN CON GOLDEN STACK")
print("═" * 80)
print(f"\n📊 Stats:")
print(f"   • Código original: {len(codigo)} caracteres")
print(f"   • Contexto: {contexto}")
print(f"\n⏳ Esto tomará 1-2 minutos...")
print("\n" + "═" * 80 + "\n")

# Ejecutar ai_duo.py
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
    salida, _ = proceso.communicate(input=contexto + "\n")
    
    print(salida)
    
    if proceso.returncode == 0:
        print("\n" + "═" * 80)
        print("✅ REFACTORIZACIÓN COMPLETADA")
        print("═" * 80)
        print("\n📋 Revisa la salida arriba para ver:")
        print("   • Arquitectura propuesta por el Arquitecto")
        print("   • Código refactorizado por el Implementador")
        print("   • Tests generados")
        print("   • Instrucciones de implementación")
    else:
        print("\n❌ Error en la refactorización")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)

