#!/usr/bin/env python3
"""
🔒 PRE-COMMIT SECURITY AUDIT
Audita tu código antes de hacer git push
Generado por: Neo-Tokyo Dev v3.0
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔒 PRE-COMMIT SECURITY AUDIT                                                ║
║  Audita tu código antes de subirlo a GitHub                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

def get_staged_files() -> list[str]:
    """Obtiene archivos en staging de git."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return []
    return [f.strip() for f in result.stdout.split('\n') if f.strip()]

def read_file_safe(filepath: str) -> Optional[str]:
    """Lee archivo de forma segura."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"⚠️  No se pudo leer {filepath}: {e}")
        return None

def audit_code(code: str, filename: str) -> None:
    """Audita el código con Neo-Tokyo Dev."""
    
    prompt = f"""Audita este código que estoy a punto de subir a GitHub.

ARCHIVO: {filename}
CÓDIGO:
{code}

ARQUITECTO (Temp 0.85 - SÉ EXTREMADAMENTE CRÍTICO Y PARANOICO):
Busca TODOS los problemas de seguridad y calidad:

🔒 SEGURIDAD:
1. SQL Injection vulnerabilities
2. XSS (Cross-Site Scripting)
3. Secretos hardcodeados (API keys, passwords, tokens)
4. Path traversal vulnerabilities
5. Command injection
6. Unsafe deserialization
7. Race conditions
8. Información sensible en logs

🐛 CÓDIGO FRÁGIL:
9. Manejo de errores inadecuado
10. Validación de inputs faltante
11. Búsquedas O(n) que podrían ser O(1)
12. Memory leaks
13. Resource leaks (archivos, conexiones)
14. Deadlocks potenciales
15. Edge cases no manejados

📝 CALIDAD:
16. Type hints faltantes
17. Docstrings faltantes
18. Variables mal nombradas
19. Funciones muy largas
20. Violaciones de SOLID

Lista CADA problema encontrado con línea específica.

IMPLEMENTADOR (Temp 0.3 - PARCHA CON PRECISIÓN):
Para CADA problema identificado:
1. Muestra la línea problemática
2. Explica el riesgo
3. Proporciona el código corregido
4. Agrega validaciones necesarias

RESULTADO: Código seguro, robusto y listo para producción.
Si el código es perfecto, di "✅ CÓDIGO APROBADO - Sin problemas detectados".
"""

    contexto = f"Auditoría de seguridad pre-commit para {filename}"
    
    print(f"\n{'═' * 70}")
    print(f"🔍 Auditando: {filename}")
    print(f"{'═' * 70}\n")
    
    try:
        # Ejecutar auditoría
        process = subprocess.Popen(
            ["python", "ai_duo.py", prompt],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8'
        )
        
        output, _ = process.communicate(input=contexto + "\n", timeout=300)
        print(output)
        
        # Verificar si hay problemas
        if "problemas detectados" in output.lower() or "vulnerabilidad" in output.lower():
            print(f"\n{Colors.RED}⚠️  ADVERTENCIA: Se encontraron problemas de seguridad{Colors.RESET}")
            print(f"{Colors.YELLOW}Revisa la auditoría arriba antes de hacer commit{Colors.RESET}\n")
            return False
        else:
            print(f"\n{Colors.GREEN}✅ Código aprobado por el Golden Stack{Colors.RESET}\n")
            return True
            
    except subprocess.TimeoutExpired:
        print(f"\n{Colors.RED}⚠️  Timeout en auditoría{Colors.RESET}\n")
        return False
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.RESET}\n")
        return False


def main():
    """Flujo principal de auditoría."""
    
    print("\n📋 Opciones:\n")
    print("1. Auditar archivos en staging (git add)")
    print("2. Auditar un archivo específico")
    print("3. Auditar todos los archivos Python del proyecto")
    
    opcion = input("\n▸ Opción (1/2/3): ").strip()
    
    files_to_audit = []
    
    if opcion == "1":
        # Archivos en staging
        files_to_audit = get_staged_files()
        if not files_to_audit:
            print(f"\n{Colors.YELLOW}No hay archivos en staging.{Colors.RESET}")
            print(f"Usa: git add <archivo> primero\n")
            sys.exit(0)
        
        # Filtrar solo archivos Python
        files_to_audit = [f for f in files_to_audit if f.endswith('.py')]
        
        if not files_to_audit:
            print(f"\n{Colors.YELLOW}No hay archivos Python en staging.{Colors.RESET}\n")
            sys.exit(0)
        
        print(f"\n✅ Archivos Python en staging: {len(files_to_audit)}")
        for f in files_to_audit:
            print(f"   • {f}")
    
    elif opcion == "2":
        # Archivo específico
        archivo = input("\n📄 Archivo a auditar: ").strip()
        if not Path(archivo).exists():
            print(f"\n{Colors.RED}❌ Archivo no encontrado{Colors.RESET}\n")
            sys.exit(1)
        files_to_audit = [archivo]
    
    elif opcion == "3":
        # Todos los Python
        files_to_audit = list(Path('.').rglob('*.py'))
        files_to_audit = [str(f) for f in files_to_audit if 'venv' not in str(f)]
        print(f"\n✅ Archivos Python encontrados: {len(files_to_audit)}")
    
    else:
        print(f"\n{Colors.RED}❌ Opción inválida{Colors.RESET}\n")
        sys.exit(1)
    
    # Confirmar
    print(f"\n⚠️  Se auditarán {len(files_to_audit)} archivo(s)")
    confirm = input("¿Continuar? (s/n): ").strip().lower()
    
    if confirm != 's':
        print(f"\n{Colors.YELLOW}Auditoría cancelada{Colors.RESET}\n")
        sys.exit(0)
    
    # Auditar cada archivo
    all_approved = True
    
    for filepath in files_to_audit:
        code = read_file_safe(filepath)
        if code is None:
            continue
        
        # Limitar tamaño (archivos muy grandes)
        if len(code) > 5000:
            print(f"\n{Colors.YELLOW}⚠️  {filepath} es muy grande ({len(code)} chars), "
                  f"auditando primeras 5000 líneas{Colors.RESET}")
            code = code[:5000]
        
        approved = audit_code(code, filepath)
        if not approved:
            all_approved = False
    
    # Resultado final
    print(f"\n{'═' * 70}")
    if all_approved:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ TODOS LOS ARCHIVOS APROBADOS{Colors.RESET}")
        print(f"{Colors.GREEN}Seguro hacer git push{Colors.RESET}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}⚠️  ALGUNOS ARCHIVOS TIENEN PROBLEMAS{Colors.RESET}")
        print(f"{Colors.YELLOW}Revisa y corrige antes de hacer push{Colors.RESET}")
    print(f"{'═' * 70}\n")


class Colors:
    """Colores para output."""
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"


if __name__ == "__main__":
    main()

