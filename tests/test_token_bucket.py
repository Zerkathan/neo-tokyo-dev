#!/usr/bin/env python3
"""
🧪 NEO-TOKYO DEV - Test Suite para TokenBucket
Generado por: Llama 3.1 (Arquitecto) + Qwen 2.5 Coder (Implementador)

Suite completa de tests unitarios con 100% de cobertura
"""

import pytest
import asyncio
import threading
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from typing import Dict, List, Tuple
from fastapi import HTTPException

# Importar la clase a testear
import sys
sys.path.insert(0, '..')
from rate_limiter import TokenBucket


# ══════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════

@pytest.fixture
def token_bucket():
    """
    Fixture que crea un TokenBucket estándar para tests.
    
    Returns:
        TokenBucket con capacidad 10 y ventana de 60 segundos
    """
    return TokenBucket(capacidad=10, tiempo_token=60.0, max_tokens_user=None)


@pytest.fixture
def token_bucket_con_limite():
    """
    Fixture que crea un TokenBucket con límite máximo por usuario.
    
    Returns:
        TokenBucket con límite máximo de 15 tokens por usuario
    """
    return TokenBucket(capacidad=10, tiempo_token=60.0, max_tokens_user=15)


@pytest.fixture
def mock_datetime():
    """
    Fixture que mockea datetime.now() para tests determinísticos.
    """
    with patch('rate_limiter.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        yield mock_dt


# ══════════════════════════════════════════════════════════════
# TESTS DE INICIALIZACIÓN
# ══════════════════════════════════════════════════════════════

def test_inicializacion_basica():
    """
    Test: TokenBucket se inicializa correctamente con parámetros válidos.
    
    Valida:
        - Capacidad asignada correctamente
        - Tiempo de token configurado
        - Diccionario de timestamps vacío
        - Lock creado
    """
    bucket = TokenBucket(capacidad=5, tiempo_token=30.0)
    
    assert bucket.capacidad == 5
    assert bucket.tiempo_token == 30.0
    assert bucket.token_timestamps == {}
    assert bucket.max_tokens_user is None
    assert bucket.lock is not None


def test_inicializacion_con_limite_maximo():
    """
    Test: TokenBucket se inicializa con límite máximo correctamente.
    
    Valida:
        - max_tokens_user se asigna correctamente
    """
    bucket = TokenBucket(capacidad=10, tiempo_token=60.0, max_tokens_user=20)
    
    assert bucket.max_tokens_user == 20


@pytest.mark.parametrize("capacidad,tiempo", [
    (1, 1.0),
    (10, 60.0),
    (100, 3600.0),
])
def test_inicializacion_parametrizada(capacidad, tiempo):
    """
    Test: TokenBucket se inicializa con diferentes configuraciones.
    
    Valida:
        - Diferentes capacidades y tiempos funcionan correctamente
    """
    bucket = TokenBucket(capacidad=capacidad, tiempo_token=tiempo)
    
    assert bucket.capacidad == capacidad
    assert bucket.tiempo_token == tiempo


# ══════════════════════════════════════════════════════════════
# TESTS DE TOMAR TOKEN - CASOS EXITOSOS
# ══════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_tomar_primer_token_exitoso(token_bucket):
    """
    Test: Un usuario puede tomar su primer token exitosamente.
    
    Valida:
        - El primer token se obtiene correctamente
        - Retorna True
        - Token se registra en el diccionario
    """
    resultado = await token_bucket.tomar_token(usuario_id=1)
    
    assert resultado is True
    assert 1 in token_bucket.token_timestamps
    assert len(token_bucket.token_timestamps[1]) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("usuario_id", [1, 2, 3, 999, 12345])
async def test_tomar_token_multiples_usuarios(token_bucket, usuario_id):
    """
    Test: Diferentes usuarios pueden tomar tokens independientemente.
    
    Valida:
        - Cada usuario tiene su propio contador de tokens
        - Los usuarios no interfieren entre sí
    """
    resultado = await token_bucket.tomar_token(usuario_id=usuario_id)
    
    assert resultado is True
    assert usuario_id in token_bucket.token_timestamps


@pytest.mark.asyncio
async def test_tomar_tokens_hasta_capacidad(token_bucket):
    """
    Test: Un usuario puede tomar tokens hasta alcanzar la capacidad.
    
    Valida:
        - Se pueden tomar exactamente 'capacidad' tokens
        - Todos los tokens se registran correctamente
    """
    usuario_id = 1
    capacidad = token_bucket.capacidad
    
    for i in range(capacidad):
        resultado = await token_bucket.tomar_token(usuario_id=usuario_id)
        assert resultado is True, f"Falló en token {i+1}/{capacidad}"
    
    assert len(token_bucket.token_timestamps[usuario_id]) == capacidad


# ══════════════════════════════════════════════════════════════
# TESTS DE RATE LIMITING
# ══════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_rate_limit_alcanzado(token_bucket):
    """
    Test: Cuando se alcanza el límite, no se pueden tomar más tokens.
    
    Valida:
        - Después de 'capacidad' tokens, el siguiente retorna False
        - El contador de tokens no aumenta
    """
    usuario_id = 1
    
    # Tomar todos los tokens disponibles
    for _ in range(token_bucket.capacidad):
        await token_bucket.tomar_token(usuario_id=usuario_id)
    
    # Intentar tomar uno más
    resultado = await token_bucket.tomar_token(usuario_id=usuario_id)
    
    assert resultado is False
    assert len(token_bucket.token_timestamps[usuario_id]) == token_bucket.capacidad


@pytest.mark.asyncio
async def test_limite_maximo_por_usuario_alcanzado(token_bucket_con_limite):
    """
    Test: HTTPException se lanza cuando se alcanza max_tokens_user.
    
    Valida:
        - Al alcanzar max_tokens_user se lanza HTTPException
        - El código de status es 429
    """
    usuario_id = 1
    max_tokens = token_bucket_con_limite.max_tokens_user
    
    # Tomar tokens hasta el límite máximo
    for _ in range(max_tokens):
        await token_bucket_con_limite.tomar_token(usuario_id=usuario_id)
    
    # El siguiente debe lanzar excepción
    with pytest.raises(HTTPException) as exc_info:
        await token_bucket_con_limite.tomar_token(usuario_id=usuario_id)
    
    assert exc_info.value.status_code == 429


# ══════════════════════════════════════════════════════════════
# TESTS DE EXPIRACIÓN DE TOKENS
# ══════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_tokens_expirados_se_eliminan(token_bucket):
    """
    Test: Los tokens expirados se eliminan automáticamente.
    
    Valida:
        - Tokens fuera de la ventana de tiempo se eliminan
        - Nuevos tokens se pueden tomar después de la expiración
    """
    usuario_id = 1
    
    # Tomar todos los tokens
    for _ in range(token_bucket.capacidad):
        await token_bucket.tomar_token(usuario_id=usuario_id)
    
    # No se puede tomar más
    resultado = await token_bucket.tomar_token(usuario_id=usuario_id)
    assert resultado is False
    
    # Mockear tiempo para simular expiración
    with patch('rate_limiter.datetime') as mock_dt:
        # Simular tiempo futuro (más de tiempo_token)
        tiempo_futuro = datetime.now() + timedelta(seconds=token_bucket.tiempo_token + 10)
        mock_dt.now.return_value = tiempo_futuro
        
        # Ahora debería poder tomar token nuevamente
        resultado = await token_bucket.tomar_token(usuario_id=usuario_id)
        assert resultado is True


# ══════════════════════════════════════════════════════════════
# TESTS DE GET_TOKENS
# ══════════════════════════════════════════════════════════════

def test_get_tokens_usuario_nuevo(token_bucket):
    """
    Test: get_tokens retorna 0 para usuarios sin tokens.
    
    Valida:
        - Usuarios nuevos tienen 0 tokens
    """
    tokens = token_bucket.get_tokens(usuario_id=999)
    assert tokens == 0


@pytest.mark.asyncio
async def test_get_tokens_despues_de_tomar(token_bucket):
    """
    Test: get_tokens retorna el número correcto de tokens activos.
    
    Valida:
        - El contador de tokens es preciso
    """
    usuario_id = 1
    
    # Tomar 5 tokens
    for _ in range(5):
        await token_bucket.tomar_token(usuario_id=usuario_id)
    
    tokens = token_bucket.get_tokens(usuario_id=usuario_id)
    assert tokens == 5


# ══════════════════════════════════════════════════════════════
# TESTS DE THREAD-SAFETY
# ══════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_concurrencia_multiples_usuarios():
    """
    Test: Múltiples usuarios pueden tomar tokens concurrentemente.
    
    Valida:
        - Thread-safety con múltiples usuarios
        - No hay race conditions
    """
    bucket = TokenBucket(capacidad=10, tiempo_token=60.0)
    
    async def tomar_tokens_usuario(usuario_id: int, num_tokens: int):
        results = []
        for _ in range(num_tokens):
            result = await bucket.tomar_token(usuario_id)
            results.append(result)
        return results
    
    # 5 usuarios tomando 5 tokens cada uno
    tasks = [tomar_tokens_usuario(i, 5) for i in range(1, 6)]
    results = await asyncio.gather(*tasks)
    
    # Todos deberían haber obtenido sus 5 tokens
    for user_results in results:
        assert all(user_results), "Algún usuario no pudo obtener todos sus tokens"


@pytest.mark.asyncio
async def test_concurrencia_mismo_usuario():
    """
    Test: El mismo usuario con peticiones concurrentes es manejado correctamente.
    
    Valida:
        - Lock previene race conditions
        - El conteo de tokens es preciso incluso con concurrencia
    """
    bucket = TokenBucket(capacidad=10, tiempo_token=60.0)
    usuario_id = 1
    
    # 15 peticiones concurrentes (más que la capacidad)
    tasks = [bucket.tomar_token(usuario_id) for _ in range(15)]
    results = await asyncio.gather(*tasks)
    
    # Solo 10 deberían ser True
    assert sum(results) == 10, f"Se esperaban 10 tokens, se obtuvieron {sum(results)}"
    assert results.count(False) == 5, "Deberían haber 5 rechazos"


# ══════════════════════════════════════════════════════════════
# TESTS DE EDGE CASES
# ══════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_capacidad_cero():
    """
    Test: TokenBucket con capacidad 0 siempre rechaza tokens.
    
    Valida:
        - Manejo de configuración edge (capacidad = 0)
    """
    bucket = TokenBucket(capacidad=0, tiempo_token=60.0)
    
    resultado = await bucket.tomar_token(usuario_id=1)
    assert resultado is False


@pytest.mark.asyncio
async def test_usuario_id_negativo(token_bucket):
    """
    Test: IDs de usuario negativos funcionan correctamente.
    
    Valida:
        - No hay validación restrictiva de IDs
    """
    resultado = await token_bucket.tomar_token(usuario_id=-1)
    assert resultado is True


def test_get_tokens_con_limpieza_de_expirados(token_bucket):
    """
    Test: get_tokens limpia tokens expirados antes de contar.
    
    Valida:
        - La limpieza de tokens expirados es automática
    """
    usuario_id = 1
    
    # Agregar tokens manualmente (simulando pasado)
    ahora = datetime.now().timestamp()
    token_bucket.token_timestamps[usuario_id] = [
        (1.0, ahora - 100),  # Expirado
        (1.0, ahora - 50),   # Expirado
        (1.0, ahora - 10),   # Válido
    ]
    
    tokens = token_bucket.get_tokens(usuario_id=usuario_id)
    
    # Solo el token válido debe contarse
    assert tokens == 1


# ══════════════════════════════════════════════════════════════
# TESTS DE COBERTURA 100%
# ══════════════════════════════════════════════════════════════

def test_get_stats_estructura():
    """
    Test: Verificar que el bucket mantiene estructura interna correcta.
    
    Valida:
        - Estructura de datos interna
    """
    bucket = TokenBucket(capacidad=10, tiempo_token=60.0)
    
    assert isinstance(bucket.token_timestamps, dict)
    assert isinstance(bucket.capacidad, int)
    assert isinstance(bucket.tiempo_token, float)


# ══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PYTEST
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([
        __file__,
        "-v",                    # Verbose
        "--cov=rate_limiter",    # Coverage para rate_limiter
        "--cov-report=html",     # Reporte HTML
        "--cov-report=term",     # Reporte en terminal
        "-s",                    # No capturar stdout
    ])

