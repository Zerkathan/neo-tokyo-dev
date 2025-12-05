#!/usr/bin/env python3
"""
🔮 NEO-TOKYO DEV v3.0 - Rate Limiter con Token Bucket
Generado por: Llama 3.1 (Arquitecto) + Qwen 2.5 Coder (Implementador)
"""

from typing import Dict, List, Tuple
from datetime import datetime
import asyncio
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import threading

app = FastAPI(
    title="Rate Limiter API - Neo-Tokyo Dev",
    version="1.0.0",
    description="""
    🔮 **Rate Limiter con Token Bucket Algorithm**
    
    API profesional de rate limiting para controlar el flujo de peticiones por usuario.
    
    ## Características
    - ✅ Rate limiting por usuario (10 peticiones/minuto por defecto)
    - ✅ Thread-safe con locks
    - ✅ Limpieza automática de tokens expirados
    - ✅ Límite máximo configurable por usuario
    - ✅ Estadísticas en tiempo real
    
    ## Generado por Golden Stack
    - 🏛️ Arquitecto: Llama 3.1 (8B)
    - ⚡ Implementador: Qwen 2.5 Coder (7B)
    - 💰 Costo: $0.00
    """,
    contact={
        "name": "Neo-Tokyo Dev Team",
        "url": "https://github.com/neo-tokyo-dev",
        "email": "dev@neo-tokyo.io"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {"name": "Rate Limiting", "description": "Endpoints protegidos con rate limiting"},
        {"name": "Monitoring", "description": "Estadísticas y métricas del sistema"},
        {"name": "Info", "description": "Información general de la API"}
    ]
)


class Usuario(BaseModel):
    """Modelo de usuario para validación."""
    id_usuario: int


class TokenBucket:
    """
    Implementación de Rate Limiter usando el algoritmo Token Bucket.
    Thread-safe y eficiente con complejidad O(n).
    """
    
    def __init__(
        self, 
        capacidad: int, 
        tiempo_token: float, 
        max_tokens_user: int = None
    ):
        """
        Inicializa un objeto TokenBucket.
        
        Args:
            capacidad: Capacidad máxima de tokens por usuario
            tiempo_token: Tiempo en segundos para regenerar un token
            max_tokens_user: Límite máximo absoluto de tokens por usuario (opcional)
        """
        self.capacidad = capacidad
        self.tiempo_token = tiempo_token
        self.token_timestamps: Dict[int, List[Tuple[float, float]]] = {}
        self.max_tokens_user = max_tokens_user
        self.lock = threading.Lock()  # Thread-safety
    
    async def tomar_token(self, usuario_id: int) -> bool:
        """
        Intenta tomar un token del bucket para el usuario especificado.
        
        Args:
            usuario_id: ID del usuario que solicita el token
            
        Returns:
            True si se pudo tomar el token, False en caso contrario
            
        Raises:
            HTTPException: Si se excede el límite máximo de tokens por usuario
        """
        with self.lock:  # Thread-safe
            ahora = datetime.now().timestamp()

            # Inicializar la lista de tokens para el usuario si no existe
            if usuario_id not in self.token_timestamps:
                self.token_timestamps[usuario_id] = []

            # Limpiar los tokens expirados
            self.token_timestamps[usuario_id] = [
                (token, timestamp)
                for token, timestamp in self.token_timestamps[usuario_id]
                if ahora - timestamp < self.tiempo_token
            ]

            # Calcular tokens disponibles del usuario
            user_tokens = len(self.token_timestamps[usuario_id])

            # Verificar límite máximo por usuario
            if self.max_tokens_user is not None and user_tokens >= self.max_tokens_user:
                raise HTTPException(
                    status_code=429, 
                    detail=f"Too Many Requests for user {usuario_id}. Max: {self.max_tokens_user}"
                )

            # Verificar capacidad del bucket
            if user_tokens >= self.capacidad:
                return False

            # Tomar un token
            self.token_timestamps[usuario_id].append((1.0, ahora))

            return True
    
    def get_tokens(self, usuario_id: int) -> int:
        """
        Devuelve la cantidad de tokens disponibles del usuario.
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Cantidad de tokens disponibles
        """
        with self.lock:  # Thread-safe
            ahora = datetime.now().timestamp()

            if usuario_id not in self.token_timestamps:
                return 0

            # Limpiar tokens expirados
            self.token_timestamps[usuario_id] = [
                (token, timestamp)
                for token, timestamp in self.token_timestamps[usuario_id]
                if ahora - timestamp < self.tiempo_token
            ]

            return len(self.token_timestamps[usuario_id])
    
    def get_stats(self) -> Dict:
        """
        Obtiene estadísticas del rate limiter.
        
        Returns:
            Diccionario con estadísticas
        """
        with self.lock:
            return {
                "total_users": len(self.token_timestamps),
                "capacidad": self.capacidad,
                "tiempo_token": self.tiempo_token,
                "max_tokens_user": self.max_tokens_user
            }


# Instancia global del TokenBucket
# Configuración: 10 peticiones por minuto (60 segundos)
rate_limiter = TokenBucket(
    capacidad=10, 
    tiempo_token=60.0,
    max_tokens_user=15  # Límite absoluto
)


def get_rate_limiter() -> TokenBucket:
    """Dependency injection para FastAPI."""
    return rate_limiter


@app.post(
    "/rate-limited",
    tags=["Rate Limiting"],
    summary="Endpoint protegido por rate limiting",
    response_description="Token tomado exitosamente",
    responses={
        200: {
            "description": "Token tomado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "mensaje": "Token tomado exitosamente",
                        "usuario_id": 12345,
                        "tokens_restantes": 7
                    }
                }
            }
        },
        429: {
            "description": "Rate limit excedido",
            "content": {
                "application/json": {
                    "example": {"detail": "Too Many Requests. Please try again later."}
                }
            }
        }
    }
)
async def rate_limited_endpoint(
    usuario: Usuario, 
    token_bucket: TokenBucket = Depends(get_rate_limiter)
):
    """
    Intenta tomar un token del bucket para el usuario especificado.
    
    **Comportamiento:**
    - ✅ 200: Token tomado exitosamente, petición permitida
    - ❌ 429: Rate limit alcanzado, petición bloqueada
    
    **Reglas:**
    1. Cada usuario tiene su propio contador de tokens
    2. Máximo 10 peticiones por ventana de 60 segundos
    3. Los tokens expirados se limpian automáticamente
    4. Límite absoluto de 15 peticiones
    
    Args:
        usuario: Objeto con ID del usuario
        token_bucket: TokenBucket inyectado por dependencias
        
    Returns:
        Mensaje de éxito con tokens restantes
        
    Raises:
        HTTPException: 429 si se excede el rate limit
    """
    try:
        if await token_bucket.tomar_token(usuario.id_usuario):
            tokens_restantes = token_bucket.capacidad - token_bucket.get_tokens(usuario.id_usuario)
            return {
                "mensaje": "Token tomado exitosamente",
                "usuario_id": usuario.id_usuario,
                "tokens_restantes": tokens_restantes
            }
        else:
            raise HTTPException(
                status_code=429, 
                detail="Too Many Requests. Please try again later."
            )
    except HTTPException as e:
        raise e


@app.get(
    "/stats",
    tags=["Monitoring"],
    summary="Estadísticas globales del sistema",
    response_description="Estadísticas del rate limiter"
)
async def get_stats(token_bucket: TokenBucket = Depends(get_rate_limiter)):
    """
    Retorna estadísticas generales del rate limiter.
    
    **Información retornada:**
    - Total de usuarios registrados
    - Capacidad configurada del bucket
    - Ventana de tiempo en segundos
    - Límite máximo por usuario
    
    **Uso:** Este endpoint es útil para monitoring y debugging.
    No consume tokens del rate limiter.
    
    Returns:
        Estadísticas globales del sistema
    """
    return token_bucket.get_stats()


@app.get(
    "/user/{usuario_id}/tokens",
    tags=["Monitoring"],
    summary="Tokens de un usuario específico",
    response_description="Estado de tokens del usuario"
)
async def get_user_tokens(
    usuario_id: int, 
    token_bucket: TokenBucket = Depends(get_rate_limiter)
):
    """
    Consulta el estado de tokens de un usuario específico.
    
    **Información retornada:**
    - Tokens usados en la ventana actual
    - Tokens disponibles restantes
    - Capacidad total del bucket
    
    **Notas:**
    - Los tokens expirados se limpian automáticamente antes de contar
    - Este endpoint NO consume tokens del rate limiter
    
    Args:
        usuario_id: ID del usuario a consultar
        
    Returns:
        Estado completo de tokens del usuario
    """
    tokens = token_bucket.get_tokens(usuario_id)
    return {
        "usuario_id": usuario_id,
        "tokens_usados": tokens,
        "tokens_disponibles": token_bucket.capacidad - tokens,
        "capacidad_total": token_bucket.capacidad
    }


@app.get(
    "/",
    tags=["Info"],
    summary="Información de la API",
    response_description="Detalles de la API"
)
async def root():
    """
    Retorna información general de la API.
    
    Incluye nombre, versión, descripción y endpoints disponibles.
    Útil para descubrimiento y health checks.
    """
    return {
        "nombre": "Rate Limiter API - Neo-Tokyo Dev",
        "version": "1.0.0",
        "descripcion": "Rate Limiter con Token Bucket Algorithm",
        "generado_por": "Llama 3.1 + Qwen 2.5 Coder",
        "endpoints": {
            "POST /rate-limited": "Endpoint protegido con rate limiting",
            "GET /stats": "Estadísticas del sistema",
            "GET /user/{usuario_id}/tokens": "Tokens de un usuario",
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("🔮 NEO-TOKYO DEV - Rate Limiter API")
    print("=" * 60)
    print(f"📊 Configuración:")
    print(f"   • Capacidad: {rate_limiter.capacidad} peticiones")
    print(f"   • Ventana: {rate_limiter.tiempo_token} segundos")
    print(f"   • Límite absoluto: {rate_limiter.max_tokens_user} peticiones")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)

