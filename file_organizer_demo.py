#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🗂️ FILE ORGANIZER DEMO - Safe demonstration version                       ║
║  Creates test folder and demonstrates file organization                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import shutil
import time
from pathlib import Path


# ══════════════════════════════════════════════════════════════════════════════
# 🎨 NEON COLORS
# ══════════════════════════════════════════════════════════════════════════════

class NeonColors:
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# ══════════════════════════════════════════════════════════════════════════════
# ⚙️ CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

CATEGORIES = {
    "Documentos": [".pdf", ".doc", ".docx", ".txt", ".xlsx"],
    "Imágenes": [".jpg", ".png", ".gif", ".svg"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Música": [".mp3", ".wav", ".flac"],
    "Archivos": [".zip", ".rar", ".7z"],
    "Instaladores": [".exe", ".msi", ".dmg"],
    "Código": [".py", ".js", ".html", ".css"],
}


# ══════════════════════════════════════════════════════════════════════════════
# 🔧 UTILITY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_category(extension: str) -> str:
    """Get category for file extension."""
    extension = extension.lower()
    for category, exts in CATEGORIES.items():
        if extension in exts:
            return category
    return "Otros"


def handle_collision(dest_path: Path) -> Path:
    """Handle filename collision by adding suffix."""
    if not dest_path.exists():
        return dest_path
    
    stem = dest_path.stem
    suffix = dest_path.suffix
    parent = dest_path.parent
    counter = 1
    
    while True:
        new_path = parent / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def organize_file(source_path: Path, base_folder: Path):
    """Organize a single file."""
    if not source_path.is_file():
        return
    
    # Get category
    extension = source_path.suffix
    category = get_category(extension)
    
    # Create category folder
    category_folder = base_folder / category
    category_folder.mkdir(exist_ok=True)
    
    # Handle collision
    dest_path = category_folder / source_path.name
    dest_path = handle_collision(dest_path)
    
    # Move file
    shutil.move(str(source_path), str(dest_path))
    
    # Log
    relative_dest = dest_path.relative_to(base_folder)
    print(f"{NeonColors.GREEN}[MOVED]{NeonColors.RESET} {source_path.name} → {NeonColors.CYAN}{relative_dest}{NeonColors.RESET}")


# ══════════════════════════════════════════════════════════════════════════════
# 🎬 DEMO
# ══════════════════════════════════════════════════════════════════════════════

def run_demo():
    """Run safe demonstration."""
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.MAGENTA}🗂️ FILE ORGANIZER DEMO - Safe Demonstration{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
    
    # Create test folder
    test_folder = Path("test_downloads")
    test_folder.mkdir(exist_ok=True)
    
    print(f"{NeonColors.YELLOW}[SETUP]{NeonColors.RESET} Created test folder: {test_folder}\n")
    
    # Create sample files
    sample_files = [
        "report.pdf",
        "presentation.pptx",
        "photo.jpg",
        "screenshot.png",
        "video.mp4",
        "song.mp3",
        "archive.zip",
        "installer.exe",
        "script.py",
        "styles.css",
        "document.txt",
        "photo.jpg",  # Duplicate to test collision
    ]
    
    print(f"{NeonColors.YELLOW}[CREATE]{NeonColors.RESET} Creating {len(sample_files)} sample files...\n")
    
    for filename in sample_files:
        file_path = test_folder / filename
        file_path.write_text(f"Sample content for {filename}")
        print(f"{NeonColors.CYAN}[CREATE]{NeonColors.RESET} {filename}")
    
    print(f"\n{NeonColors.CYAN}{'─' * 78}{NeonColors.RESET}\n")
    print(f"{NeonColors.YELLOW}[ORGANIZE]{NeonColors.RESET} Starting organization...\n")
    
    time.sleep(1)
    
    # Organize all files
    files_to_organize = list(test_folder.glob("*"))
    files_to_organize = [f for f in files_to_organize if f.is_file()]
    
    for file_path in files_to_organize:
        organize_file(file_path, test_folder)
    
    # Show results
    print(f"\n{NeonColors.CYAN}{'─' * 78}{NeonColors.RESET}\n")
    print(f"{NeonColors.GREEN}[COMPLETE]{NeonColors.RESET} Organization complete!\n")
    
    print(f"{NeonColors.YELLOW}[RESULTS]{NeonColors.RESET} Folder structure:\n")
    
    # Display folder tree
    for category_folder in sorted(test_folder.iterdir()):
        if category_folder.is_dir():
            files_in_category = list(category_folder.glob("*"))
            print(f"{NeonColors.MAGENTA}📁 {category_folder.name}/{NeonColors.RESET} ({len(files_in_category)} files)")
            for file in sorted(files_in_category):
                print(f"   {NeonColors.CYAN}└─{NeonColors.RESET} {file.name}")
    
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.GREEN}[SUCCESS]{NeonColors.RESET} Demo completed successfully")
    print(f"{NeonColors.YELLOW}[INFO]{NeonColors.RESET} Test folder: {test_folder.absolute()}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print(f"\n{NeonColors.YELLOW}[ABORT]{NeonColors.RESET} Demo interrupted")
    except Exception as e:
        print(f"\n{NeonColors.RED}[ERROR]{NeonColors.RESET} {e}")

