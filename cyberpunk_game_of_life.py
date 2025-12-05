#!/usr/bin/env python3
"""
🔮 CYBERPUNK GAME OF LIFE
Conway's Game of Life con reglas cyberpunk
Generado por: Neo-Tokyo Dev v3.0 Golden Stack
"""

import numpy as np
import time
import os
import sys
import signal
from typing import Tuple, Dict
from dataclasses import dataclass
from enum import IntEnum

# ══════════════════════════════════════════════════════════════════════════════
# 🎨 ANSI COLORS
# ══════════════════════════════════════════════════════════════════════════════

class Colors:
    """Códigos ANSI para terminal cyberpunk."""
    RESET = "\033[0m"
    GREEN = "\033[92m"      # Células vivas
    RED = "\033[91m"        # Células corruptas
    CYAN = "\033[96m"       # Firewalls
    YELLOW = "\033[93m"     # Encriptadas
    DIM = "\033[2m"         # Células muertas
    BOLD = "\033[1m"
    
    @staticmethod
    def clear_screen() -> None:
        """Limpia la pantalla."""
        print("\033[2J\033[H", end="")


# ══════════════════════════════════════════════════════════════════════════════
# 📊 CELL STATES
# ══════════════════════════════════════════════════════════════════════════════

class CellState(IntEnum):
    """Estados posibles de las células."""
    DEAD = 0
    ALIVE = 1
    CORRUPTED = 2
    FIREWALL = 3
    ENCRYPTED = 4
    GLITCHED = 5  # Estado temporal


@dataclass
class CellSymbols:
    """Símbolos Unicode para cada estado."""
    DEAD: str = "░"
    ALIVE: str = "█"
    CORRUPTED: str = "☠"
    FIREWALL: str = "🛡"
    ENCRYPTED: str = "🔒"
    GLITCHED: str = "⚡"


# ══════════════════════════════════════════════════════════════════════════════
# 🎮 CYBERPUNK GAME OF LIFE
# ══════════════════════════════════════════════════════════════════════════════

class CyberpunkGameOfLife:
    """
    Conway's Game of Life con reglas cyberpunk.
    
    Reglas Base (Conway):
    1. Célula viva con <2 vecinas vivas → muere (soledad)
    2. Célula viva con 2-3 vecinas vivas → sobrevive
    3. Célula viva con >3 vecinas vivas → muere (sobrepoblación)
    4. Célula muerta con exactamente 3 vecinas vivas → nace
    
    Reglas Cyberpunk:
    1. CORRUPCIÓN: 1% probabilidad de que célula viva se corrompa
    2. CORRUPTA mata todas sus vecinas vivas (radius 1)
    3. GLITCH: 0.5% probabilidad de flip temporal de estado
    4. FIREWALL: Células especiales inmunes a corrupción
    5. ENCRYPTED: Células que no pueden ser afectadas por nada
    """
    
    def __init__(
        self,
        width: int = 80,
        height: int = 40,
        corruption_prob: float = 0.01,
        glitch_prob: float = 0.005,
        initial_density: float = 0.3,
        seed: int = None
    ):
        """
        Inicializa el juego.
        
        Args:
            width: Ancho de la cuadrícula
            height: Alto de la cuadrícula
            corruption_prob: Probabilidad de corrupción (default 1%)
            glitch_prob: Probabilidad de glitch (default 0.5%)
            initial_density: Densidad inicial de células vivas
            seed: Semilla para reproducibilidad
        """
        self.width = width
        self.height = height
        self.corruption_prob = corruption_prob
        self.glitch_prob = glitch_prob
        
        # Matrices de estado
        if seed is not None:
            np.random.seed(seed)
        
        # Estado actual
        self.grid = np.zeros((height, width), dtype=np.int8)
        
        # Inicializar con células aleatorias
        alive_mask = np.random.random((height, width)) < initial_density
        self.grid[alive_mask] = CellState.ALIVE
        
        # Agregar algunos firewalls (5% de células vivas)
        firewall_positions = np.random.random((height, width)) < 0.05
        self.grid[firewall_positions & alive_mask] = CellState.FIREWALL
        
        # Agregar algunas células encriptadas (2% de células vivas)
        encrypted_positions = np.random.random((height, width)) < 0.02
        self.grid[encrypted_positions & alive_mask] = CellState.ENCRYPTED
        
        # Estadísticas
        self.generation = 0
        self.total_corruptions = 0
        self.total_glitches = 0
        
        # Control de ejecución
        self.running = True
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, sig, frame):
        """Maneja Ctrl+C gracefully."""
        self.running = False
        print(f"\n\n{Colors.YELLOW}Simulación pausada.{Colors.RESET}")
    
    def count_alive_neighbors(self, y: int, x: int) -> int:
        """
        Cuenta vecinas vivas (estado ALIVE).
        
        Args:
            y: Fila
            x: Columna
            
        Returns:
            Número de vecinas vivas (0-8)
        """
        # Extraer vecindario 3x3
        y_min = max(0, y - 1)
        y_max = min(self.height, y + 2)
        x_min = max(0, x - 1)
        x_max = min(self.width, x + 2)
        
        neighborhood = self.grid[y_min:y_max, x_min:x_max]
        
        # Contar células vivas (excluyendo la célula central)
        alive_count = np.sum(neighborhood == CellState.ALIVE)
        if self.grid[y, x] == CellState.ALIVE:
            alive_count -= 1
        
        return alive_count
    
    def apply_corruption(self, new_grid: np.ndarray) -> None:
        """
        Aplica la regla de CORRUPCIÓN DE DATOS.
        
        Células corruptas matan todas sus vecinas vivas.
        """
        corrupted_cells = np.argwhere(self.grid == CellState.CORRUPTED)
        
        for y, x in corrupted_cells:
            # Matar todas las vecinas vivas (radius 1)
            y_min = max(0, y - 1)
            y_max = min(self.height, y + 2)
            x_min = max(0, x - 1)
            x_max = min(self.width, x + 2)
            
            for ny in range(y_min, y_max):
                for nx in range(x_min, x_max):
                    if new_grid[ny, nx] == CellState.ALIVE:
                        # Firewall y Encrypted son inmunes
                        if self.grid[ny, nx] not in [CellState.FIREWALL, CellState.ENCRYPTED]:
                            new_grid[ny, nx] = CellState.DEAD
    
    def apply_glitch(self, new_grid: np.ndarray) -> None:
        """
        Aplica GLITCHES aleatorios.
        
        Células pueden cambiar de estado temporalmente.
        """
        glitch_mask = np.random.random(new_grid.shape) < self.glitch_prob
        
        for y, x in np.argwhere(glitch_mask):
            # No afectar Encrypted ni Firewall
            if self.grid[y, x] not in [CellState.ENCRYPTED, CellState.FIREWALL]:
                # Flip estado: viva ↔ muerta
                if new_grid[y, x] == CellState.ALIVE:
                    new_grid[y, x] = CellState.DEAD
                elif new_grid[y, x] == CellState.DEAD:
                    new_grid[y, x] = CellState.ALIVE
                
                self.total_glitches += 1
    
    def step(self) -> None:
        """
        Ejecuta un paso de la simulación.
        
        Aplica reglas de Conway + reglas cyberpunk.
        """
        new_grid = self.grid.copy()
        
        # Aplicar reglas de Conway
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y, x]
                
                # Células especiales no aplican reglas de Conway
                if cell in [CellState.FIREWALL, CellState.ENCRYPTED]:
                    continue
                
                # Células corruptas persisten (no aplican Conway)
                if cell == CellState.CORRUPTED:
                    continue
                
                # Contar vecinas vivas
                alive_neighbors = self.count_alive_neighbors(y, x)
                
                # Reglas de Conway
                if cell == CellState.ALIVE:
                    # Muerte por soledad o sobrepoblación
                    if alive_neighbors < 2 or alive_neighbors > 3:
                        new_grid[y, x] = CellState.DEAD
                    # Supervivencia
                    else:
                        # Probabilidad de CORRUPCIÓN
                        if np.random.random() < self.corruption_prob:
                            new_grid[y, x] = CellState.CORRUPTED
                            self.total_corruptions += 1
                
                elif cell == CellState.DEAD:
                    # Nacimiento
                    if alive_neighbors == 3:
                        new_grid[y, x] = CellState.ALIVE
        
        # Aplicar reglas cyberpunk
        self.apply_corruption(new_grid)
        self.apply_glitch(new_grid)
        
        self.grid = new_grid
        self.generation += 1
    
    def get_statistics(self) -> Dict[str, int]:
        """Obtiene estadísticas actuales."""
        return {
            "generation": self.generation,
            "alive": np.sum(self.grid == CellState.ALIVE),
            "corrupted": np.sum(self.grid == CellState.CORRUPTED),
            "firewall": np.sum(self.grid == CellState.FIREWALL),
            "encrypted": np.sum(self.grid == CellState.ENCRYPTED),
            "total": self.width * self.height,
            "total_corruptions": self.total_corruptions,
            "total_glitches": self.total_glitches,
        }
    
    def render(self) -> str:
        """
        Renderiza el estado actual con colores.
        
        Returns:
            String con la cuadrícula coloreada
        """
        symbols = CellSymbols()
        output = []
        
        # Header
        output.append(f"{Colors.BOLD}{Colors.CYAN}╔{'═' * (self.width + 2)}╗{Colors.RESET}")
        output.append(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} " +
                     f"{Colors.MAGENTA}CYBERPUNK GAME OF LIFE{Colors.RESET}" +
                     f" {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
        output.append(f"{Colors.BOLD}{Colors.CYAN}╚{'═' * (self.width + 2)}╝{Colors.RESET}\n")
        
        # Grid
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                cell = self.grid[y, x]
                
                if cell == CellState.ALIVE:
                    row += f"{Colors.GREEN}{symbols.ALIVE}{Colors.RESET}"
                elif cell == CellState.CORRUPTED:
                    row += f"{Colors.RED}{Colors.BOLD}{symbols.CORRUPTED}{Colors.RESET}"
                elif cell == CellState.FIREWALL:
                    row += f"{Colors.CYAN}{symbols.FIREWALL}{Colors.RESET}"
                elif cell == CellState.ENCRYPTED:
                    row += f"{Colors.YELLOW}{symbols.ENCRYPTED}{Colors.RESET}"
                else:  # DEAD
                    row += f"{Colors.DIM}{symbols.DEAD}{Colors.RESET}"
            
            output.append(row)
        
        # Stats
        stats = self.get_statistics()
        output.append(f"\n{Colors.BOLD}{Colors.CYAN}╔{'═' * 60}╗{Colors.RESET}")
        output.append(
            f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} "
            f"{Colors.YELLOW}Gen:{Colors.RESET} {stats['generation']:<4} │ "
            f"{Colors.GREEN}█ Vivas:{Colors.RESET} {stats['alive']:<5} │ "
            f"{Colors.RED}☠ Corruptas:{Colors.RESET} {stats['corrupted']:<4} │ "
            f"{Colors.CYAN}🛡 Firewalls:{Colors.RESET} {stats['firewall']:<3} │ "
            f"{Colors.YELLOW}🔒 Encriptadas:{Colors.RESET} {stats['encrypted']:<3}"
        )
        output.append(
            f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} "
            f"Corrupciones totales: {Colors.RED}{stats['total_corruptions']}{Colors.RESET} │ "
            f"Glitches totales: {Colors.MAGENTA}{stats['total_glitches']}{Colors.RESET}"
        )
        output.append(f"{Colors.BOLD}{Colors.CYAN}╚{'═' * 60}╝{Colors.RESET}")
        
        # Leyenda
        output.append(f"\n{Colors.DIM}Leyenda: "
                     f"{Colors.GREEN}█{Colors.RESET} Viva │ "
                     f"{Colors.DIM}░{Colors.RESET} Muerta │ "
                     f"{Colors.RED}☠{Colors.RESET} Corrupta │ "
                     f"{Colors.CYAN}🛡{Colors.RESET} Firewall │ "
                     f"{Colors.YELLOW}🔒{Colors.RESET} Encriptada"
                     f"{Colors.DIM}")
        output.append(f"Presiona Ctrl+C para detener{Colors.RESET}\n")
        
        return "\n".join(output)
    
    def run(self, fps: int = 10, max_generations: int = None) -> None:
        """
        Ejecuta la simulación.
        
        Args:
            fps: Frames por segundo (velocidad de animación)
            max_generations: Generaciones máximas (None = infinito)
        """
        delay = 1.0 / fps
        
        try:
            while self.running:
                # Limpiar pantalla y renderizar
                Colors.clear_screen()
                print(self.render())
                
                # Step
                self.step()
                
                # Verificar límite de generaciones
                if max_generations and self.generation >= max_generations:
                    break
                
                # Delay para animación
                time.sleep(delay)
                
                # Verificar si todo está muerto o corrupto
                stats = self.get_statistics()
                if stats['alive'] == 0 and stats['corrupted'] == 0:
                    print(f"\n{Colors.RED}Sistema colapsado - Todas las células murieron{Colors.RESET}")
                    break
        
        except KeyboardInterrupt:
            pass
        finally:
            # Estadísticas finales
            self._print_final_stats()
    
    def _print_final_stats(self) -> None:
        """Imprime estadísticas finales."""
        stats = self.get_statistics()
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}╔{'═' * 60}╗{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{'  ESTADÍSTICAS FINALES':^60}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}╠{'═' * 60}╣{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} Generaciones: {stats['generation']:<47} {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} Células vivas finales: {Colors.GREEN}{stats['alive']:<38}{Colors.RESET} {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} Células corruptas finales: {Colors.RED}{stats['corrupted']:<33}{Colors.RESET} {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} Total de corrupciones: {stats['total_corruptions']:<39} {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} Total de glitches: {stats['total_glitches']:<43} {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}╚{'═' * 60}╝{Colors.RESET}\n")


# ══════════════════════════════════════════════════════════════════════════════
# 🎮 MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Punto de entrada principal."""
    print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║{Colors.MAGENTA}  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗███╗   ██╗██╗  ██╗{Colors.CYAN}║
║{Colors.MAGENTA}  ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔══██╗██║   ██║████╗  ██║██║ ██╔╝{Colors.CYAN}║
║{Colors.MAGENTA}  ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██████╔╝██║   ██║██╔██╗ ██║█████╔╝ {Colors.CYAN}║
║{Colors.MAGENTA}  ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██╔═══╝ ██║   ██║██║╚██╗██║██╔═██╗ {Colors.CYAN}║
║{Colors.MAGENTA}  ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║     ╚██████╔╝██║ ╚████║██║  ██╗{Colors.CYAN}║
║{Colors.MAGENTA}   ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝{Colors.CYAN}║
║                                                                      ║
║{Colors.YELLOW}              🔮 GAME OF LIFE - CYBERPUNK EDITION 🔮              {Colors.CYAN}║
║{Colors.GREEN}                 Generado por Neo-Tokyo Dev v3.0                  {Colors.CYAN}║
╚══════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.YELLOW}Reglas del juego:{Colors.RESET}

{Colors.GREEN}Conway's Game of Life:{Colors.RESET}
• Célula viva con <2 vecinas → muere (soledad)
• Célula viva con 2-3 vecinas → sobrevive
• Célula viva con >3 vecinas → muere (sobrepoblación)
• Célula muerta con 3 vecinas → nace

{Colors.RED}Reglas Cyberpunk:{Colors.RESET}
• {Colors.RED}CORRUPCIÓN{Colors.RESET}: 1% probabilidad de que célula se corrompa
• {Colors.RED}☠ Corruptas{Colors.RESET} matan todas sus vecinas vivas
• {Colors.MAGENTA}GLITCH{Colors.RESET}: 0.5% probabilidad de flip de estado
• {Colors.CYAN}🛡 Firewall{Colors.RESET}: Inmunes a corrupción
• {Colors.YELLOW}🔒 Encriptadas{Colors.RESET}: Inmunes a todo

{Colors.CYAN}Iniciando simulación en 3 segundos...{Colors.RESET}
""")
    
    time.sleep(3)
    
    # Crear y ejecutar juego
    game = CyberpunkGameOfLife(
        width=60,
        height=30,
        corruption_prob=0.01,
        glitch_prob=0.005,
        initial_density=0.35,
        seed=None  # None = aleatorio, o número para reproducible
    )
    
    game.run(fps=10, max_generations=None)
    
    print(f"{Colors.GREEN}Gracias por jugar Cyberpunk Game of Life!{Colors.RESET}")
    print(f"{Colors.CYAN}Generado por: Neo-Tokyo Dev v3.0 Golden Stack{Colors.RESET}\n")


if __name__ == "__main__":
    main()

