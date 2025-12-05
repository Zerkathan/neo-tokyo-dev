#!/usr/bin/env python3
"""
Script de prueba para el Rate Limiter API
"""
import requests
import time
from rich.console import Console
from rich.table import Table

console = Console()

BASE_URL = "http://localhost:8000"


def test_rate_limiter():
    """Prueba el rate limiter con múltiples peticiones."""
    
    console.print("\n🔮 [cyan]Neo-Tokyo Dev - Rate Limiter Test[/cyan]")
    console.print("=" * 60)
    
    # 1. Info del API
    console.print("\n[yellow]📋 Información del API:[/yellow]")
    response = requests.get(f"{BASE_URL}/")
    info = response.json()
    console.print(f"  • Nombre: {info['nombre']}")
    console.print(f"  • Versión: {info['version']}")
    console.print(f"  • Generado por: {info['generado_por']}")
    
    # 2. Estadísticas iniciales
    console.print("\n[yellow]📊 Estadísticas del sistema:[/yellow]")
    stats = requests.get(f"{BASE_URL}/stats").json()
    console.print(f"  • Capacidad: {stats['capacidad']} peticiones")
    console.print(f"  • Ventana: {stats['tiempo_token']} segundos")
    console.print(f"  • Límite máximo: {stats['max_tokens_user']} peticiones")
    console.print(f"  • Usuarios totales: {stats['total_users']}")
    
    # 3. Probar rate limiting
    console.print("\n[yellow]🚀 Probando Rate Limiting (Usuario 1):[/yellow]")
    console.print("Enviando 15 peticiones...")
    
    tabla = Table(title="Resultados de Peticiones")
    tabla.add_column("#", style="cyan")
    tabla.add_column("Status", style="green")
    tabla.add_column("Tokens Restantes", style="yellow")
    tabla.add_column("Mensaje", style="white")
    
    for i in range(1, 16):
        try:
            response = requests.post(
                f"{BASE_URL}/rate-limited",
                json={"id_usuario": 1},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                tabla.add_row(
                    str(i),
                    "✅ 200",
                    str(data.get('tokens_restantes', 'N/A')),
                    data.get('mensaje', '')
                )
            else:
                tabla.add_row(
                    str(i),
                    f"❌ {response.status_code}",
                    "0",
                    response.json().get('detail', 'Error')
                )
        except Exception as e:
            tabla.add_row(str(i), "⚠️  Error", "?", str(e))
        
        time.sleep(0.1)  # Pequeña pausa
    
    console.print(tabla)
    
    # 4. Verificar tokens del usuario
    console.print("\n[yellow]👤 Tokens del Usuario 1:[/yellow]")
    tokens = requests.get(f"{BASE_URL}/user/1/tokens").json()
    console.print(f"  • Tokens usados: {tokens['tokens_usados']}")
    console.print(f"  • Tokens disponibles: {tokens['tokens_disponibles']}")
    console.print(f"  • Capacidad total: {tokens['capacidad_total']}")
    
    # 5. Probar con otro usuario
    console.print("\n[yellow]🚀 Probando con Usuario 2 (3 peticiones):[/yellow]")
    for i in range(1, 4):
        response = requests.post(
            f"{BASE_URL}/rate-limited",
            json={"id_usuario": 2}
        )
        if response.status_code == 200:
            console.print(f"  ✅ Petición {i}: Éxito")
        else:
            console.print(f"  ❌ Petición {i}: Rate limited")
    
    # 6. Estadísticas finales
    console.print("\n[yellow]📊 Estadísticas finales:[/yellow]")
    stats = requests.get(f"{BASE_URL}/stats").json()
    console.print(f"  • Usuarios totales: {stats['total_users']}")
    
    console.print("\n" + "=" * 60)
    console.print("[green]✅ Test completado![/green]\n")


if __name__ == "__main__":
    try:
        test_rate_limiter()
    except requests.exceptions.ConnectionError:
        console.print("\n[red]❌ Error: El servidor no está corriendo[/red]")
        console.print("[yellow]Ejecuta primero: python rate_limiter.py[/yellow]\n")
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]\n")

