#!/usr/bin/env python3
"""
⛓️ MINI-BLOCKCHAIN EDUCATIVA
Blockchain básica para entender el concepto
Generado por: Neo-Tokyo Dev v3.0 Golden Stack
"""

import hashlib
import datetime
from typing import List, Optional


# ══════════════════════════════════════════════════════════════════════════════
# 🎨 COLORES
# ══════════════════════════════════════════════════════════════════════════════

class Colors:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"


# ══════════════════════════════════════════════════════════════════════════════
# 🧱 BLOQUE (Block)
# ══════════════════════════════════════════════════════════════════════════════

class Block:
    """
    Representa un bloque individual en la blockchain.
    
    Conceptos clave:
    - Hash: Huella digital única del bloque
    - Previous Hash: Enlace al bloque anterior (crea la "cadena")
    - Nonce: Número que cambiamos hasta encontrar un hash válido
    - Proof of Work: El proceso de encontrar el nonce correcto
    """
    
    def __init__(
        self,
        index: int,
        data: str,
        previous_hash: str,
        difficulty: int = 4
    ):
        """
        Crea un nuevo bloque.
        
        Args:
            index: Número del bloque en la cadena
            data: Información almacenada en el bloque
            previous_hash: Hash del bloque anterior (crea el enlace)
            difficulty: Número de ceros requeridos al inicio del hash
        """
        self.index = index
        self.timestamp = datetime.datetime.now()
        self.data = data
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.nonce = 0  # Proof of Work
        self.hash = ""
        
        # Minar el bloque (Proof of Work)
        self._mine_block()
    
    def _calculate_hash(self) -> str:
        """
        Calcula el hash SHA-256 del bloque.
        
        El hash incluye TODOS los datos del bloque + el nonce.
        Si cambias cualquier dato, el hash cambia completamente.
        Esto garantiza la inmutabilidad de la blockchain.
        """
        block_string = (
            str(self.index) +
            str(self.timestamp) +
            self.data +
            self.previous_hash +
            str(self.nonce)
        )
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def _mine_block(self) -> None:
        """
        Mina el bloque (Proof of Work).
        
        Proof of Work:
        - Busca un nonce que haga que el hash comience con N ceros
        - Esto requiere probar miles/millones de combinaciones
        - Es computacionalmente costoso a propósito
        - Hace que la blockchain sea segura (costoso alterar)
        
        Ejemplo:
        - Difficulty 2: hash debe empezar con "00..."
        - Difficulty 4: hash debe empezar con "0000..."
        - Más ceros = más difícil = más seguro
        """
        target = "0" * self.difficulty
        
        print(f"{Colors.YELLOW}⛏️  Minando bloque #{self.index}...{Colors.RESET}", end=" ")
        
        while True:
            self.hash = self._calculate_hash()
            
            # ¿El hash cumple la dificultad?
            if self.hash.startswith(target):
                # ¡Encontrado!
                print(f"{Colors.GREEN}✅ Nonce encontrado: {self.nonce}{Colors.RESET}")
                break
            
            # No cumple, probar siguiente nonce
            self.nonce += 1
            
            # Mostrar progreso cada 100K intentos
            if self.nonce % 100000 == 0:
                print(f"{self.nonce:,}", end="...", flush=True)
    
    def __str__(self) -> str:
        """Representación bonita del bloque."""
        return f"""
{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} {Colors.BOLD}Bloque #{self.index}{Colors.RESET}
{Colors.BOLD}{Colors.CYAN}╠══════════════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} {Colors.YELLOW}Timestamp:{Colors.RESET}     {self.timestamp}
{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} {Colors.GREEN}Data:{Colors.RESET}          {self.data}
{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} {Colors.MAGENTA}Previous Hash:{Colors.RESET} {self.previous_hash[:16]}...
{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} {Colors.CYAN}Nonce:{Colors.RESET}         {self.nonce:,}
{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} {Colors.GREEN}Hash:{Colors.RESET}          {self.hash[:16]}...
{Colors.BOLD}{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""


# ══════════════════════════════════════════════════════════════════════════════
# ⛓️ BLOCKCHAIN (Chain)
# ══════════════════════════════════════════════════════════════════════════════

class Blockchain:
    """
    La blockchain completa - una cadena de bloques enlazados.
    
    Conceptos clave:
    - Cada bloque apunta al anterior (cadena)
    - Cambiar un bloque rompe toda la cadena posterior
    - Esto hace la blockchain inmutable
    """
    
    def __init__(self, difficulty: int = 4):
        """
        Inicializa la blockchain con el bloque génesis.
        
        Args:
            difficulty: Dificultad del Proof of Work (4 = 4 ceros al inicio)
        """
        self.chain: List[Block] = []
        self.difficulty = difficulty
        
        # Crear bloque génesis (el primero de la cadena)
        self._create_genesis_block()
    
    def _create_genesis_block(self) -> None:
        """
        Crea el bloque génesis (el primero de la cadena).
        
        El bloque génesis es especial:
        - No tiene bloque anterior
        - Es el origen de toda la cadena
        """
        genesis = Block(
            index=0,
            data="Genesis Block - El Origen de Neo-Tokyo Chain",
            previous_hash="0" * 64,  # Hash ficticio (64 ceros)
            difficulty=self.difficulty
        )
        self.chain.append(genesis)
    
    def get_latest_block(self) -> Block:
        """Obtiene el último bloque de la cadena."""
        return self.chain[-1]
    
    def add_block(self, data: str) -> Block:
        """
        Agrega un nuevo bloque a la cadena.
        
        Args:
            data: Información a almacenar en el bloque
            
        Returns:
            El bloque creado
        """
        latest = self.get_latest_block()
        
        new_block = Block(
            index=len(self.chain),
            data=data,
            previous_hash=latest.hash,
            difficulty=self.difficulty
        )
        
        self.chain.append(new_block)
        return new_block
    
    def is_valid(self) -> bool:
        """
        Valida la integridad de toda la blockchain.
        
        Verifica:
        1. Cada bloque enlaza correctamente al anterior
        2. Ningún bloque ha sido modificado (hash válido)
        3. Todos los bloques cumplen la dificultad
        
        Returns:
            True si la cadena es válida, False si hay manipulación
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            # Verificar que el previous_hash coincide
            if current.previous_hash != previous.hash:
                print(f"{Colors.RED}❌ Cadena rota en bloque #{i}{Colors.RESET}")
                return False
            
            # Verificar que el hash es correcto
            if current.hash != current._calculate_hash():
                print(f"{Colors.RED}❌ Bloque #{i} ha sido manipulado{Colors.RESET}")
                return False
            
            # Verificar proof of work
            target = "0" * current.difficulty
            if not current.hash.startswith(target):
                print(f"{Colors.RED}❌ Proof of work inválido en bloque #{i}{Colors.RESET}")
                return False
        
        print(f"{Colors.GREEN}✅ Blockchain válida - Ninguna manipulación detectada{Colors.RESET}")
        return True
    
    def print_chain(self) -> None:
        """Imprime toda la cadena de bloques."""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}═" * 70 + f"{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}BLOCKCHAIN - {len(self.chain)} BLOQUES{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}═" * 70 + f"{Colors.RESET}\n")
        
        for block in self.chain:
            print(block)
        
        # Estadísticas
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 ESTADÍSTICAS:{Colors.RESET}")
        print(f"   • Total de bloques: {len(self.chain)}")
        print(f"   • Dificultad: {self.difficulty} ceros")
        print(f"   • Cadena válida: ", end="")
        self.is_valid()
        print()


# ══════════════════════════════════════════════════════════════════════════════
# 🎮 DEMO INTERACTIVA
# ══════════════════════════════════════════════════════════════════════════════

def demo_blockchain():
    """Demo educativa de blockchain."""
    
    print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║{Colors.MAGENTA}  ███╗   ███╗██╗███╗   ██╗██╗       ██████╗██╗  ██╗ █████╗ ██╗███╗   ██╗  {Colors.CYAN}║
║{Colors.MAGENTA}  ████╗ ████║██║████╗  ██║██║      ██╔════╝██║  ██║██╔══██╗██║████╗  ██║  {Colors.CYAN}║
║{Colors.MAGENTA}  ██╔████╔██║██║██╔██╗ ██║██║█████╗██║     ███████║███████║██║██╔██╗ ██║  {Colors.CYAN}║
║{Colors.MAGENTA}  ██║╚██╔╝██║██║██║╚██╗██║██║╚════╝██║     ██╔══██║██╔══██║██║██║╚██╗██║  {Colors.CYAN}║
║{Colors.MAGENTA}  ██║ ╚═╝ ██║██║██║ ╚████║██║      ╚██████╗██║  ██║██║  ██║██║██║ ╚████║  {Colors.CYAN}║
║{Colors.MAGENTA}  ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝       ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝  {Colors.CYAN}║
║                                                                      ║
║{Colors.YELLOW}              🔮 Blockchain Educativa - Neo-Tokyo Dev 🔮            {Colors.CYAN}║
╚══════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.BOLD}¿Qué es Blockchain?{Colors.RESET}
Imagina una {Colors.CYAN}cadena de postales{Colors.RESET} donde cada postal:
• Tiene un número (index)
• Contiene un mensaje (data)
• Tiene un código secreto (hash)
• Hace referencia al código de la postal anterior (previous_hash)

Si intentas cambiar una postal antigua, su código cambia, y TODAS
las postales posteriores se invalidan. {Colors.GREEN}¡Eso es inmutabilidad!{Colors.RESET}

{Colors.BOLD}Proof of Work (Minado):{Colors.RESET}
Para agregar un bloque, debes {Colors.YELLOW}encontrar un número mágico (nonce){Colors.RESET}
que haga que el hash comience con varios ceros (ej: 0000abc123...).
Esto requiere {Colors.RED}miles de intentos{Colors.RESET} = es costoso = es seguro.

{Colors.CYAN}Iniciando demostración...{Colors.RESET}
""")
    
    # Crear blockchain
    print(f"\n{Colors.BOLD}Creando blockchain con dificultad 4...{Colors.RESET}\n")
    blockchain = Blockchain(difficulty=4)
    
    # Agregar bloques
    print(f"{Colors.BOLD}\nAgregando transacciones a la blockchain:{Colors.RESET}\n")
    
    blockchain.add_block("Alice envía 10 BTC a Bob")
    blockchain.add_block("Bob envía 5 BTC a Charlie")
    blockchain.add_block("Charlie envía 2 BTC a Alice")
    
    # Mostrar blockchain
    blockchain.print_chain()
    
    # Demo de manipulación
    print(f"\n{Colors.BOLD}{Colors.RED}🔥 DEMO: Intentando manipular la blockchain...{Colors.RESET}\n")
    print(f"{Colors.YELLOW}Cambiando data del bloque #1...{Colors.RESET}")
    
    original_data = blockchain.chain[1].data
    blockchain.chain[1].data = "Alice envía 1000 BTC a Alice (FRAUDE!)"
    
    print(f"{Colors.MAGENTA}¿La blockchain sigue siendo válida?{Colors.RESET}\n")
    blockchain.is_valid()
    
    # Restaurar
    blockchain.chain[1].data = original_data
    print(f"\n{Colors.GREEN}Restaurando data original...{Colors.RESET}\n")
    blockchain.is_valid()
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}✨ ¡Así funciona blockchain!{Colors.RESET}")
    print(f"{Colors.CYAN}Inmutable. Transparente. Descentralizada.{Colors.RESET}\n")


if __name__ == "__main__":
    demo_blockchain()

