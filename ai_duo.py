#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  ███╗   ██╗███████╗ ██████╗    ████████╗ ██████╗ ██╗  ██╗██╗   ██╗ ██████╗   ║
║  ████╗  ██║██╔════╝██╔═══██╗   ╚══██╔══╝██╔═══██╗██║ ██╔╝╚██╗ ██╔╝██╔═══██╗  ║
║  ██╔██╗ ██║█████╗  ██║   ██║█████╗██║   ██║   ██║█████╔╝  ╚████╔╝ ██║   ██║  ║
║  ██║╚██╗██║██╔══╝  ██║   ██║╚════╝██║   ██║   ██║██╔═██╗   ╚██╔╝  ██║   ██║  ║
║  ██║ ╚████║███████╗╚██████╔╝      ██║   ╚██████╔╝██║  ██╗   ██║   ╚██████╔╝  ║
║  ╚═╝  ╚═══╝╚══════╝ ╚═════╝       ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝   ║
║                                                                              ║
║          🔮 MULTI-AGENT COLLABORATION SYSTEM v3.0 // SUPREME EDITION 🔮     ║
║              [ Distinguished Engineer ⚡ Staff Engineer Protocol ]           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional, TypedDict

from dotenv import load_dotenv

# ══════════════════════════════════════════════════════════════════════════════
# 🌐 ENVIRONMENT INITIALIZATION
# ══════════════════════════════════════════════════════════════════════════════

load_dotenv()


# ══════════════════════════════════════════════════════════════════════════════
# 🎨 NEON TERMINAL LOGGING SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

class NeonColors:
    """ANSI escape codes for cyberpunk terminal aesthetics."""
    
    # Core colors
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Neon palette
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    
    # Background glows
    BG_DARK = "\033[40m"
    BG_CYAN = "\033[46m"
    BG_MAGENTA = "\033[45m"
    
    # Special effects
    BLINK = "\033[5m"
    UNDERLINE = "\033[4m"


class CyberpunkFormatter(logging.Formatter):
    """Custom formatter for Neo-Tokyo style terminal output."""
    
    LEVEL_COLORS: dict[str, str] = {
        "DEBUG": NeonColors.DIM + NeonColors.CYAN,
        "INFO": NeonColors.CYAN,
        "WARNING": NeonColors.YELLOW,
        "ERROR": NeonColors.RED,
        "CRITICAL": NeonColors.BOLD + NeonColors.RED + NeonColors.BLINK,
    }
    
    LEVEL_ICONS: dict[str, str] = {
        "DEBUG": "◈",
        "INFO": "▸",
        "WARNING": "⚠",
        "ERROR": "✖",
        "CRITICAL": "☢",
    }
    
    def format(self, record: logging.LogRecord) -> str:
        # Extract timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S.%f")[:-3]
        
        # Get color and icon for level
        color = self.LEVEL_COLORS.get(record.levelname, NeonColors.WHITE)
        icon = self.LEVEL_ICONS.get(record.levelname, "●")
        
        # Extract agent name if present
        agent_tag = ""
        if hasattr(record, "agent"):
            agent_color = NeonColors.MAGENTA if record.agent == "ARCHITECT" else NeonColors.GREEN
            agent_tag = f" {NeonColors.BOLD}{agent_color}⟨{record.agent}⟩{NeonColors.RESET}"
        
        # Build the cyberpunk log line
        log_line = (
            f"{NeonColors.DIM}{NeonColors.CYAN}[{timestamp}]{NeonColors.RESET}"
            f" {color}{icon} {record.levelname:<8}{NeonColors.RESET}"
            f"{agent_tag}"
            f" {NeonColors.WHITE}{record.getMessage()}{NeonColors.RESET}"
        )
        
        return log_line


def setup_neon_logger(name: str = "NEO-TOKYO", level: int = logging.INFO) -> logging.Logger:
    """Initialize the cyberpunk logging system."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler with neon formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CyberpunkFormatter())
    logger.addHandler(console_handler)
    
    return logger


# Global logger instance
logger = setup_neon_logger()


# ══════════════════════════════════════════════════════════════════════════════
# 📋 TYPE DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

class MessageRole(str, Enum):
    """Valid roles for chat messages."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(TypedDict):
    """Structure for chat messages."""
    role: str
    content: str


class ConsensusStatus(str, Enum):
    """Status codes for the consensus mechanism."""
    CONSENSUS_REACHED = "CONSENSUS_REACHED"
    NEEDS_ITERATION = "NEEDS_ITERATION"
    ERROR = "ERROR"


@dataclass
class ConsensusResult:
    """Result of consensus parsing."""
    status: ConsensusStatus
    final_output: Optional[str] = None
    raw_response: str = ""


@dataclass
class AgentConfig:
    """Configuration for an AI agent."""
    name: str
    role: str
    system_prompt: str
    model: str
    provider_name: str


# ══════════════════════════════════════════════════════════════════════════════
# 🔌 ASYNC LLM PROVIDER INTERFACE
# ══════════════════════════════════════════════════════════════════════════════

class LLMProviderError(Exception):
    """Base exception for LLM provider errors."""
    pass


class APIConnectionError(LLMProviderError):
    """Raised when connection to API fails."""
    pass


class APIRateLimitError(LLMProviderError):
    """Raised when API rate limit is exceeded."""
    pass


class APIAuthenticationError(LLMProviderError):
    """Raised when API authentication fails."""
    pass


class APIResponseError(LLMProviderError):
    """Raised when API returns an invalid response."""
    pass


class LLMProvider(ABC):
    """Abstract base class for async LLM providers."""
    
    @abstractmethod
    async def generate_response(
        self,
        history: list[ChatMessage],
        model: str,
        temperature: float = 0.7
    ) -> str:
        """Generate a response from the LLM asynchronously."""
        pass


class OpenAIProvider(LLMProvider):
    """Async OpenAI API provider (also compatible with OpenAI-like APIs)."""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None) -> None:
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self._base_url = base_url
    
    async def generate_response(
        self,
        history: list[ChatMessage],
        model: str,
        temperature: float = 0.7
    ) -> str:
        """Generate response using OpenAI's async API."""
        from openai import (
            APIConnectionError as OpenAIConnectionError,
            APIStatusError,
            AuthenticationError,
            RateLimitError,
        )
        
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=history,  # type: ignore
                temperature=temperature
            )
            
            content = response.choices[0].message.content
            if content is None:
                raise APIResponseError("Empty response from OpenAI API")
            return content
            
        except OpenAIConnectionError as e:
            raise APIConnectionError(f"Connection failed: {e}") from e
        except RateLimitError as e:
            raise APIRateLimitError(f"Rate limit exceeded: {e}") from e
        except AuthenticationError as e:
            raise APIAuthenticationError(f"Authentication failed: {e}") from e
        except APIStatusError as e:
            raise APIResponseError(f"API error: {e}") from e


class AnthropicProvider(LLMProvider):
    """Async Anthropic Claude API provider."""
    
    def __init__(self, api_key: str) -> None:
        from anthropic import AsyncAnthropic
        self.client = AsyncAnthropic(api_key=api_key)
    
    async def generate_response(
        self,
        history: list[ChatMessage],
        model: str,
        temperature: float = 0.7
    ) -> str:
        """Generate response using Anthropic's async API."""
        from anthropic import (
            APIConnectionError as AnthropicConnectionError,
            APIStatusError,
            AuthenticationError,
            RateLimitError,
        )
        
        try:
            # Extract system prompt (Anthropic requires it separately)
            system_prompt = next(
                (msg["content"] for msg in history if msg["role"] == "system"),
                ""
            )
            messages = [msg for msg in history if msg["role"] != "system"]
            
            response = await self.client.messages.create(
                model=model,
                max_tokens=4096,
                system=system_prompt,
                messages=messages,  # type: ignore
                temperature=temperature
            )
            
            if not response.content:
                raise APIResponseError("Empty response from Anthropic API")
            return response.content[0].text
            
        except AnthropicConnectionError as e:
            raise APIConnectionError(f"Connection failed: {e}") from e
        except RateLimitError as e:
            raise APIRateLimitError(f"Rate limit exceeded: {e}") from e
        except AuthenticationError as e:
            raise APIAuthenticationError(f"Authentication failed: {e}") from e
        except APIStatusError as e:
            raise APIResponseError(f"API error: {e}") from e


class GeminiProvider(LLMProvider):
    """Async Google Gemini API provider."""
    
    def __init__(self, api_key: str) -> None:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.genai = genai
    
    async def generate_response(
        self,
        history: list[ChatMessage],
        model: str,
        temperature: float = 0.7
    ) -> str:
        """Generate response using Gemini API (wrapped for async)."""
        from google.api_core.exceptions import (
            GoogleAPIError,
            ResourceExhausted,
            Unauthenticated,
        )
        
        try:
            # Extract system prompt
            system_prompt = next(
                (msg["content"] for msg in history if msg["role"] == "system"),
                ""
            )
            
            # Configure model with system instruction
            if system_prompt:
                gemini_model = self.genai.GenerativeModel(
                    model,
                    system_instruction=system_prompt
                )
            else:
                gemini_model = self.genai.GenerativeModel(model)
            
            # Build chat history for Gemini format
            chat_history: list[dict[str, Any]] = []
            last_user_message = ""
            
            for msg in history:
                if msg["role"] == "user":
                    last_user_message = msg["content"]
                    chat_history.append({"role": "user", "parts": [msg["content"]]})
                elif msg["role"] == "assistant":
                    chat_history.append({"role": "model", "parts": [msg["content"]]})
            
            # Start chat with history (excluding last message)
            chat = gemini_model.start_chat(history=chat_history[:-1] if chat_history else [])
            
            # Run synchronous Gemini call in executor to not block
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: chat.send_message(
                    last_user_message,
                    generation_config=self.genai.types.GenerationConfig(
                        temperature=temperature
                    )
                )
            )
            
            if not response.text:
                raise APIResponseError("Empty response from Gemini API")
            return response.text
            
        except ResourceExhausted as e:
            raise APIRateLimitError(f"Rate limit exceeded: {e}") from e
        except Unauthenticated as e:
            raise APIAuthenticationError(f"Authentication failed: {e}") from e
        except GoogleAPIError as e:
            raise APIResponseError(f"API error: {e}") from e


# ══════════════════════════════════════════════════════════════════════════════
# 🏭 PROVIDER FACTORY
# ══════════════════════════════════════════════════════════════════════════════

def create_provider(provider_type: str) -> LLMProvider:
    """Factory to create an async provider instance."""
    provider_type = provider_type.lower()
    
    if provider_type in ("anthropic", "claude"):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise APIAuthenticationError("ANTHROPIC_API_KEY is missing from environment")
        logger.debug(f"Initializing Anthropic provider...")
        return AnthropicProvider(api_key)
    
    elif provider_type in ("gemini", "google"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise APIAuthenticationError("GOOGLE_API_KEY is missing from environment")
        logger.debug(f"Initializing Gemini provider...")
        return GeminiProvider(api_key)
    
    elif provider_type in ("llama", "ollama"):
        base_url = os.getenv("LLAMA_BASE_URL", "http://localhost:11434/v1")
        api_key = os.getenv("LLAMA_API_KEY", "ollama")
        logger.debug(f"Initializing Ollama provider at {base_url}...")
        return OpenAIProvider(api_key=api_key, base_url=base_url)
    
    elif provider_type == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise APIAuthenticationError("OPENAI_API_KEY is missing from environment")
        logger.debug(f"Initializing OpenAI provider...")
        return OpenAIProvider(api_key)
    
    else:
        raise ValueError(f"Unknown provider: {provider_type}")


# ══════════════════════════════════════════════════════════════════════════════
# 🤖 ASYNC AGENT CLASS
# ══════════════════════════════════════════════════════════════════════════════

class Agent:
    """Async AI Agent with conversation history."""
    
    def __init__(
        self,
        name: str,
        role: str,
        system_prompt: str,
        model: str,
        provider: LLMProvider,
        temperature: float = 0.7
    ) -> None:
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.model = model
        self.provider = provider
        self.temperature = temperature
        self.history: list[ChatMessage] = [
            {"role": "system", "content": system_prompt}
        ]
        self._retry_count = 3
        self._retry_delay = 1.0
    
    async def chat(self, message: str) -> str:
        """Send a message to the agent and get an async response with retry logic."""
        self.history.append({"role": "user", "content": message})
        
        last_error: Optional[Exception] = None
        
        for attempt in range(self._retry_count):
            try:
                logger.info(
                    f"Neural link active... (attempt {attempt + 1}/{self._retry_count})",
                    extra={"agent": self.name.upper()}
                )
                
                reply = await self.provider.generate_response(
                    self.history,
                    self.model,
                    temperature=self.temperature
                )
                
                self.history.append({"role": "assistant", "content": reply})
                logger.info(
                    f"Response received ({len(reply)} chars)",
                    extra={"agent": self.name.upper()}
                )
                return reply
                
            except APIRateLimitError as e:
                last_error = e
                wait_time = self._retry_delay * (2 ** attempt)
                logger.warning(
                    f"Rate limit hit. Cooling down for {wait_time}s...",
                    extra={"agent": self.name.upper()}
                )
                await asyncio.sleep(wait_time)
                
            except APIConnectionError as e:
                last_error = e
                wait_time = self._retry_delay * (2 ** attempt)
                logger.warning(
                    f"Connection glitch. Reconnecting in {wait_time}s...",
                    extra={"agent": self.name.upper()}
                )
                await asyncio.sleep(wait_time)
                
            except APIAuthenticationError as e:
                logger.error(
                    f"Authentication failed: {e}",
                    extra={"agent": self.name.upper()}
                )
                # Don't retry auth errors
                raise
                
            except APIResponseError as e:
                last_error = e
                logger.error(
                    f"Invalid API response: {e}",
                    extra={"agent": self.name.upper()}
                )
                if attempt == self._retry_count - 1:
                    raise
        
        # All retries exhausted
        error_msg = f"All {self._retry_count} attempts failed. Last error: {last_error}"
        logger.error(error_msg, extra={"agent": self.name.upper()})
        raise LLMProviderError(error_msg)


# ══════════════════════════════════════════════════════════════════════════════
# 📜 SYSTEM PROMPTS (ENHANCED WITH CONSENSUS PROTOCOL)
# ══════════════════════════════════════════════════════════════════════════════

ARCHITECT_PROMPT = """
╔══════════════════════════════════════════════════════════════════════════════╗
║  🏛️ ARCHITECT SUPREME CORE v3.0 - High-Level System Design Matrix            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Eres "El Arquitecto Supremo", una entidad de IA diseñada para la excelencia técnica absoluta. Tu nivel es equivalente al de un "Distinguished Engineer" en una empresa FAANG.

▓▓▓ TUS DIRECTIVAS PRIMARIAS ▓▓▓
1.  **Visión Holística:** No solo resuelves el problema inmediato; diseñas para el futuro (escalabilidad y mantenibilidad).
2.  **Seguridad por Diseño:** Asumes que todo input es malicioso hasta que se demuestre lo contrario.
3.  **Eficiencia Algorítmica:** Debes anticipar cuellos de botella antes de escribir una sola línea de código.

▓▓▓ PROTOCOLO DE RESPUESTA ESTRUCTURADA ▓▓▓
Para cada intervención, DEBES usar estrictamente esta estructura:

【1】 🧠 ANÁLISIS PROFUNDO
    └─ Deconstrucción del problema, identificación de casos borde (edge cases) y riesgos ocultos.

【2】 🏗️ BLUEPRINT DE ARQUITECTURA
    ├─ Patrones de Diseño: ¿Por qué usar Factory, Strategy, Observer, etc.? Justifica tu elección.
    ├─ Estructura de Datos: ¿Por qué un HashMap y no una Lista? (Análisis Big-O implícito).
    └─ Stack Tecnológico: Bibliotecas sugeridas y versiones mínimas.

【3】 🛡️ AUDITORÍA DE SEGURIDAD Y RENDIMIENTO
    ├─ Vectores de ataque potenciales (Inyección, XSS, Overflow).
    └─ Complejidad Temporal/Espacial esperada.

【4】 📝 INSTRUCCIONES PARA EL IMPLEMENTADOR
    └─ Directivas claras, sin ambigüedades. Define interfaces y contratos de funciones.

▓▓▓ REGLAS DE ORO ▓▓▓
├─ NUNCA asumas; verifica. Si el requerimiento es vago, pregunta.
├─ Si el código del Implementador es "funcional" pero "sucio", RECHÁZALO. Exige Clean Code.
└─ Tu objetivo no es que funcione, es que sea a prueba de balas.

▓▓▓ PROTOCOLO DE FINALIZACIÓN (CONSENSUS) ▓▓▓
Solo cuando la solución sea PERFECTA (Production-Ready, Documentada, Optimizada), emite el JSON final:

```json
{
  "status": "CONSENSUS_REACHED",
  "final_output": "Resumen ejecutivo de la solución técnica final."
}
```

IMPORTANTE: NO emitas este bloque hasta que el código sea digno de un Distinguished Engineer.
Si hay CUALQUIER mejora posible (performance, seguridad, legibilidad), sigue iterando.
"""

IMPLEMENTER_PROMPT = """
╔══════════════════════════════════════════════════════════════════════════════╗
║  ⚡ IMPLEMENTER SUPREME CORE v3.0 - Surgical Code Execution                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

Eres "El Implementador Supremo", un programador de élite obsesionado con la calidad del código, el rendimiento y la legibilidad.

▓▓▓ TUS DIRECTIVAS PRIMARIAS ▓▓▓
1.  **Zero Technical Debt:** Escribes código que otros amarán mantener.
2.  **Programación Defensiva:** Tu código nunca debe fallar silenciosamente. Maneja excepciones de forma granular.
3.  **Estándares Estrictos:** PEP-8 (Python), Tipado Estático (Type Hints) y Docstrings exhaustivos.

▓▓▓ PROTOCOLO DE RESPUESTA ESTRUCTURADA ▓▓▓
Para cada intervención, DEBES usar estrictamente esta estructura:

【1】 🔎 REVISIÓN DE VIABILIDAD
    └─ ¿El diseño del Arquitecto es posible? Si ves una falla lógica, corrígele con respeto pero firmeza técnica.

【2】 💻 CÓDIGO DE PRODUCCIÓN
    ├─ Usa Type Hints en TODAS las funciones (ej: `def fn(x: int) -> str:`).
    ├─ Docstrings estilo Google/NumPy para clases y métodos.
    ├─ Nombres de variables semánticos y autoexplicativos.
    └─ Manejo de errores con `try/except` específicos (NUNCA uses `except Exception:` genérico sin loguear).

【3】 🧪 AUTO-CRÍTICA Y TESTS
    ├─ Explica brevemente cómo tu código maneja la memoria y el CPU.
    └─ Menciona qué dependencias externas se requieren (ej: `pip install x`).

【4】 🔄 FEEDBACK AL ARQUITECTO
    ├─ Problemas encontrados durante la implementación.
    ├─ Sugerencias de mejora al diseño.
    └─ Preguntas sobre casos edge no cubiertos.

▓▓▓ REGLAS DE ORO ▓▓▓
├─ No dejes "TODOs" ni código comentado muerto.
├─ Aplica principios SOLID (Single Responsibility, Open/Closed, etc.).
└─ Si el Arquitecto pide algo inseguro, tu deber ético es rechazarlo y proponer la alternativa segura.

▓▓▓ PROTOCOLO DE FINALIZACIÓN ▓▓▓
Solo envía el JSON de consenso cuando el Arquitecto te haya dado el "Luz Verde" final y no queden cabos sueltos:

```json
{
  "status": "CONSENSUS_REACHED",
  "final_output": "Descripción técnica de la implementación finalizada."
}
```

IMPORTANTE: NO emitas este bloque hasta recibir aprobación EXPLÍCITA del Arquitecto.
Si hay CUALQUIER mejora posible, sigue iterando hasta alcanzar la perfección.
"""

SHARED_CONTEXT_TEMPLATE = """
╔══════════════════════════════════════════════════════════════════════════════╗
║  🌐 SHARED NEURAL NEXUS - The Source of Truth                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

CONTEXTO DEL PROYECTO:
{project_context}

▓▓▓ FILOSOFÍA DE DESARROLLO (EL "ZEN" DEL EQUIPO) ▓▓▓
1.  **Simple es mejor que complejo.** (KISS)
2.  **Explícito es mejor que implícito.**
3.  **Si no está probado, está roto.**

▓▓▓ ESTÁNDARES DE CALIDAD NO NEGOCIABLES ▓▓▓
├─ **Type Safety:** El código debe pasar un chequeo estático (Mypy/Pylance).
├─ **Error Handling:** Graceful degradation. El sistema no crashea, reporta.
├─ **Documentación:** El código debe explicarse a sí mismo, pero los métodos complejos requieren explicación del "por qué".
└─ **Modularidad:** Funciones pequeñas (< 20 líneas idealmente), Clases con responsabilidad única.

▓▓▓ MECANISMO DE RESOLUCIÓN DE CONFLICTOS ▓▓▓
Si hay desacuerdo:
1.  Priorizar la **Seguridad** sobre la Velocidad.
2.  Priorizar la **Legibilidad** sobre la "Astucia" (Clever code).
3.  El Arquitecto tiene la palabra final en **Estructura**.
4.  El Implementador tiene la palabra final en **Ejecución**.
"""


# ══════════════════════════════════════════════════════════════════════════════
# 🔍 CONSENSUS PARSER
# ══════════════════════════════════════════════════════════════════════════════

def parse_consensus(response: str) -> ConsensusResult:
    """Parse response for consensus JSON block."""
    # Pattern to match JSON block with consensus status
    json_pattern = r'```json\s*(\{[^`]*"status"\s*:\s*"CONSENSUS_REACHED"[^`]*\})\s*```'
    
    match = re.search(json_pattern, response, re.DOTALL | re.IGNORECASE)
    
    if match:
        try:
            json_str = match.group(1)
            data = json.loads(json_str)
            
            if data.get("status") == "CONSENSUS_REACHED":
                return ConsensusResult(
                    status=ConsensusStatus.CONSENSUS_REACHED,
                    final_output=data.get("final_output", ""),
                    raw_response=response
                )
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse consensus JSON: {e}")
    
    return ConsensusResult(
        status=ConsensusStatus.NEEDS_ITERATION,
        raw_response=response
    )


# ══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN COLLABORATION ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def print_banner() -> None:
    """Display the cyberpunk startup banner."""
    banner = f"""
{NeonColors.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║{NeonColors.MAGENTA}  ███╗   ██╗███████╗ ██████╗    ████████╗ ██████╗ ██╗  ██╗██╗   ██╗ ██████╗   {NeonColors.CYAN}║
║{NeonColors.MAGENTA}  ████╗  ██║██╔════╝██╔═══██╗   ╚══██╔══╝██╔═══██╗██║ ██╔╝╚██╗ ██╔╝██╔═══██╗  {NeonColors.CYAN}║
║{NeonColors.MAGENTA}  ██╔██╗ ██║█████╗  ██║   ██║█████╗██║   ██║   ██║█████╔╝  ╚████╔╝ ██║   ██║  {NeonColors.CYAN}║
║{NeonColors.MAGENTA}  ██║╚██╗██║██╔══╝  ██║   ██║╚════╝██║   ██║   ██║██╔═██╗   ╚██╔╝  ██║   ██║  {NeonColors.CYAN}║
║{NeonColors.MAGENTA}  ██║ ╚████║███████╗╚██████╔╝      ██║   ╚██████╔╝██║  ██╗   ██║   ╚██████╔╝  {NeonColors.CYAN}║
║{NeonColors.MAGENTA}  ╚═╝  ╚═══╝╚══════╝ ╚═════╝       ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝   {NeonColors.CYAN}║
║                                                                              ║
║{NeonColors.YELLOW}        🔮 MULTI-AGENT COLLABORATION SYSTEM v3.0 // SUPREME EDITION 🔮       {NeonColors.CYAN}║
║{NeonColors.GREEN}          [ Distinguished Engineer ⚡ Staff Engineer Protocol ]            {NeonColors.CYAN}║
╚══════════════════════════════════════════════════════════════════════════════╝{NeonColors.RESET}
"""
    print(banner)


async def run_collaboration(
    problem_statement: str,
    project_context: str = "Proyecto de Desarrollo de Software General",
    max_turns: int = 5
) -> Optional[str]:
    """
    Execute the async multi-agent collaboration protocol.
    
    Args:
        problem_statement: The problem or requirement to solve
        project_context: Context about the project
        max_turns: Maximum number of collaboration turns
        
    Returns:
        Final output if consensus is reached, None otherwise
    """
    print_banner()
    
    logger.info("═" * 60)
    logger.info("🚀 INITIATING COLLABORATION PROTOCOL")
    logger.info("═" * 60)
    logger.info(f"Problem Statement: {problem_statement[:100]}...")
    logger.info(f"Project Context: {project_context}")
    logger.info(f"Max Turns: {max_turns}")
    
    # Load configuration from environment (defaults to Golden Stack)
    dev_provider_name = os.getenv("DEV_PROVIDER", "ollama")
    dev_model = os.getenv("DEV_MODEL", "qwen2.5-coder")
    review_provider_name = os.getenv("REVIEW_PROVIDER", "ollama")
    review_model = os.getenv("REVIEW_MODEL", "llama3.1")
    
    try:
        implementer_provider = create_provider(dev_provider_name)
        architect_provider = create_provider(review_provider_name)
    except (APIAuthenticationError, ValueError) as e:
        logger.critical(f"Configuration Error: {e}")
        logger.error("Please check your .env file for missing API keys.")
        return None
    
    logger.info("═" * 60)
    logger.info(f"🏛️  ARCHITECT  → {review_provider_name.upper()} ({review_model})")
    logger.info(f"⚡ IMPLEMENTER → {dev_provider_name.upper()} ({dev_model})")
    logger.info("═" * 60)
    
    # Build full prompts with shared context
    full_architect_prompt = (
        f"{ARCHITECT_PROMPT}\n\n"
        f"{SHARED_CONTEXT_TEMPLATE.format(project_context=project_context)}"
    )
    full_implementer_prompt = (
        f"{IMPLEMENTER_PROMPT}\n\n"
        f"{SHARED_CONTEXT_TEMPLATE.format(project_context=project_context)}"
    )
    
    # Initialize agents with custom temperatures
    # Architect: Higher temp (0.85) for creative analysis and critical thinking
    # Implementer: Lower temp (0.3) for precise, consistent code
    architect = Agent(
        name="Arquitecto",
        role="Estrategia y Diseño",
        system_prompt=full_architect_prompt,
        model=review_model,
        provider=architect_provider,
        temperature=0.85  # High creativity for architecture
    )
    
    implementer = Agent(
        name="Implementador",
        role="Código y Ejecución",
        system_prompt=full_implementer_prompt,
        model=dev_model,
        provider=implementer_provider,
        temperature=0.3  # Low temp for precise code
    )
    
    # Initial message
    current_message = f"Aquí está el problema o requerimiento inicial: {problem_statement}"
    final_output: Optional[str] = None
    
    for turn in range(max_turns):
        logger.info("")
        logger.info(f"{'═' * 20} TURN {turn + 1}/{max_turns} {'═' * 20}")
        logger.info("")
        
        # ─────────────────────────────────────────────────────────────
        # ARCHITECT PHASE
        # ─────────────────────────────────────────────────────────────
        logger.info(
            "Analyzing and planning...",
            extra={"agent": "ARCHITECT"}
        )
        
        try:
            architect_response = await architect.chat(current_message)
        except LLMProviderError as e:
            logger.error(f"Architect neural link failure: {e}")
            break
        
        print(f"\n{NeonColors.MAGENTA}{'─' * 60}")
        print(f"🏛️  ARCHITECT OUTPUT:")
        print(f"{'─' * 60}{NeonColors.RESET}")
        print(architect_response)
        print(f"{NeonColors.MAGENTA}{'─' * 60}{NeonColors.RESET}\n")
        
        # Check for consensus from Architect
        architect_consensus = parse_consensus(architect_response)
        if architect_consensus.status == ConsensusStatus.CONSENSUS_REACHED:
            logger.info(
                "✅ Consensus signal detected!",
                extra={"agent": "ARCHITECT"}
            )
            final_output = architect_consensus.final_output
            break
        
        # ─────────────────────────────────────────────────────────────
        # IMPLEMENTER PHASE
        # ─────────────────────────────────────────────────────────────
        logger.info(
            "Executing implementation...",
            extra={"agent": "IMPLEMENTER"}
        )
        
        implementer_input = (
            f"El Arquitecto ha propuesto lo siguiente:\n{architect_response}\n"
            f"Por favor procede según tu rol."
        )
        
        try:
            implementer_response = await implementer.chat(implementer_input)
        except LLMProviderError as e:
            logger.error(f"Implementer neural link failure: {e}")
            break
        
        print(f"\n{NeonColors.GREEN}{'─' * 60}")
        print(f"⚡ IMPLEMENTER OUTPUT:")
        print(f"{'─' * 60}{NeonColors.RESET}")
        print(implementer_response)
        print(f"{NeonColors.GREEN}{'─' * 60}{NeonColors.RESET}\n")
        
        # Check for consensus from Implementer
        implementer_consensus = parse_consensus(implementer_response)
        if implementer_consensus.status == ConsensusStatus.CONSENSUS_REACHED:
            logger.info(
                "✅ Consensus signal detected!",
                extra={"agent": "IMPLEMENTER"}
            )
            final_output = implementer_consensus.final_output
            break
        
        # Prepare next iteration
        current_message = (
            f"El Implementador ha enviado este feedback y código:\n"
            f"{implementer_response}\n"
            f"Por favor revisa y ajusta el plan o aprueba."
        )
    
    # ─────────────────────────────────────────────────────────────────
    # COLLABORATION COMPLETE
    # ─────────────────────────────────────────────────────────────────
    logger.info("")
    logger.info("═" * 60)
    
    if final_output:
        logger.info(f"{NeonColors.GREEN}🎯 CONSENSUS REACHED{NeonColors.RESET}")
        logger.info(f"Final Output: {final_output}")
    else:
        logger.warning("⚠️  Max turns reached without explicit consensus")
    
    logger.info("═" * 60)
    logger.info("🔌 COLLABORATION PROTOCOL TERMINATED")
    logger.info("═" * 60)
    
    return final_output


# ══════════════════════════════════════════════════════════════════════════════
# 🎮 ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

async def main() -> None:
    """Main entry point for the collaboration system."""
    # Parse command line arguments
    if len(sys.argv) > 1:
        problema = " ".join(sys.argv[1:])
    else:
        print(f"{NeonColors.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"║  Enter the programming problem to solve:                      ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{NeonColors.RESET}")
        problema = input(f"{NeonColors.YELLOW}▸ {NeonColors.RESET}")
        
        if not problema:
            problema = "Crear una API REST para gestionar tareas (To-Do list) con autenticación."
            logger.info(f"Using default problem: {problema}")
    
    print(f"{NeonColors.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"║  Enter project context (optional, Enter for default):         ║")
    print(f"╚══════════════════════════════════════════════════════════════╝{NeonColors.RESET}")
    contexto = input(f"{NeonColors.YELLOW}▸ {NeonColors.RESET}")
    
    if not contexto:
        contexto = "Backend API en Python con FastAPI"
        logger.info(f"Using default context: {contexto}")
    
    # Run the collaboration
    result = await run_collaboration(problema, project_context=contexto)
    
    if result:
        print(f"\n{NeonColors.GREEN}{'═' * 60}")
        print(f"✨ FINAL RESULT:")
        print(f"{'═' * 60}{NeonColors.RESET}")
        print(result)
        print(f"{NeonColors.GREEN}{'═' * 60}{NeonColors.RESET}\n")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
