#!/usr/bin/env python3
"""
🔮 NEO-TOKYO DEV // Quick Test Examples
Test cases for the Multi-Agent Collaboration System v3.0
"""

# Example problems to test the system

EXAMPLE_PROBLEMS = {
    "easy": "Crear una función que valide emails con regex y maneje casos edge",
    
    "medium": "Implementar un sistema de caché LRU (Least Recently Used) thread-safe en Python con complejidad O(1) para get/put",
    
    "hard": "Diseñar e implementar un rate limiter distribuido usando sliding window que soporte múltiples usuarios concurrentes",
    
    "architecture": "Diseñar la arquitectura de un sistema de streaming de video en tiempo real que soporte 100K usuarios concurrentes con baja latencia (<100ms)",
    
    "security": "Implementar un sistema de autenticación JWT con refresh tokens, protección contra CSRF y rate limiting",
    
    "performance": "Optimizar una función que procesa 10M de registros, actualmente tarda 5 minutos. Necesita reducirse a <30 segundos"
}

if __name__ == "__main__":
    print("🔮 NEO-TOKYO DEV - Test Examples\n")
    print("Copy and paste one of these problems to test the system:\n")
    
    for difficulty, problem in EXAMPLE_PROBLEMS.items():
        print(f"[{difficulty.upper()}]")
        print(f"  python ai_duo.py \"{problem}\"\n")
    
    print("\n" + "="*80)
    print("TIP: Start with 'easy' to see the system in action!")
    print("="*80)

