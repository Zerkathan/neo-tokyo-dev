#!/usr/bin/env python3
"""
Script helper para ejecutar tests del sistema sin input manual
"""
import subprocess
import sys

# Problema desafiante
PROBLEM = """Diseñar e implementar una función de hash consistente (consistent hashing) 
para distribuir claves entre N servidores. Debe manejar la adición y eliminación 
de servidores sin redistribuir todas las claves. Incluir réplicas virtuales para 
mejor balanceo y métodos para obtener estadísticas de distribución."""

CONTEXT = "Sistema distribuido de alta disponibilidad con FastAPI"

print("🔮 NEO-TOKYO DEV v3.0 - Test Automático")
print("=" * 70)
print(f"\n📋 PROBLEMA:\n{PROBLEM}")
print(f"\n🌐 CONTEXTO: {CONTEXT}")
print("\n" + "=" * 70)
print("\n🚀 Iniciando colaboración...\n")

# Ejecutar con context pipe
process = subprocess.Popen(
    ["python", "ai_duo.py", PROBLEM],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

# Enviar context
output, _ = process.communicate(input=CONTEXT + "\n")

print(output)
sys.exit(process.returncode)

