#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🗂️ FILE ORGANIZER - Automatic Downloads Manager                           ║
║  Real-time file monitoring and auto-categorization                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import shutil
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ══════════════════════════════════════════════════════════════════════════════
# 🎨 NEON COLORS
# ══════════════════════════════════════════════════════════════════════════════

class NeonColors:
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# ══════════════════════════════════════════════════════════════════════════════
# ⚙️ CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

CONFIG = {
    # Folder to monitor (defaults to user's Downloads)
    "watch_folder": str(Path.home() / "Downloads"),
    
    # Extension to category mapping
    "categories": {
        # Documents
        "Documentos": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".tex", ".xlsx", ".xls", ".pptx", ".ppt"],
        
        # Images
        "Imágenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"],
        
        # Videos
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
        
        # Music
        "Música": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
        
        # Archives
        "Archivos": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
        
        # Installers
        "Instaladores": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".apk"],
        
        # Code
        "Código": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".go", ".rs", ".ts"],
        
        # Other
        "Otros": []  # Catch-all for unknown extensions
    },
    
    # Logging
    "log_file": "file_organizer.log",
    "log_to_console": True,
}


# ══════════════════════════════════════════════════════════════════════════════
# 📝 LOGGING SETUP
# ══════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    filename=CONFIG["log_file"],
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def log_and_print(message: str, level: str = "info", color: str = NeonColors.GREEN):
    """Log to file and optionally print to console with colors."""
    # Log to file
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)
    
    # Print to console
    if CONFIG["log_to_console"]:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{NeonColors.CYAN}[{timestamp}]{NeonColors.RESET} {color}{message}{NeonColors.RESET}")


# ══════════════════════════════════════════════════════════════════════════════
# 🗂️ FILE OPERATIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_extension_category(extension: str) -> str:
    """Get category for file extension."""
    extension = extension.lower()
    
    for category, extensions in CONFIG["categories"].items():
        if extension in extensions:
            return category
    
    return "Otros"


def handle_name_collision(dest_path: Path) -> Path:
    """
    Handle filename collision by adding suffix.
    file.pdf → file_1.pdf → file_2.pdf, etc.
    """
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


def organize_file(filepath: str):
    """
    Organize a file into appropriate category folder.
    """
    try:
        source_path = Path(filepath)
        
        # Skip if file doesn't exist or is a directory
        if not source_path.exists() or source_path.is_dir():
            return
        
        # Skip hidden files and temp files
        if source_path.name.startswith('.') or source_path.name.startswith('~'):
            return
        
        # Skip if file is still being written (wait for stable size)
        try:
            initial_size = source_path.stat().st_size
            time.sleep(0.5)
            if source_path.stat().st_size != initial_size:
                log_and_print(f"SKIP: {source_path.name} (still being written)", "info", NeonColors.YELLOW)
                return
        except:
            return
        
        # Get extension and category
        extension = source_path.suffix
        category = get_extension_category(extension)
        
        # Create category folder
        watch_folder = Path(CONFIG["watch_folder"])
        category_folder = watch_folder / category
        category_folder.mkdir(exist_ok=True)
        
        # Handle name collision
        dest_path = category_folder / source_path.name
        dest_path = handle_name_collision(dest_path)
        
        # Move file
        shutil.move(str(source_path), str(dest_path))
        
        # Log success
        relative_dest = dest_path.relative_to(watch_folder)
        log_and_print(
            f"MOVED: {source_path.name} → {relative_dest}",
            "info",
            NeonColors.GREEN
        )
        
    except Exception as e:
        log_and_print(f"ERROR: {filepath} - {str(e)}", "error", NeonColors.RED)


# ══════════════════════════════════════════════════════════════════════════════
# 👁️ FILE SYSTEM WATCHER
# ══════════════════════════════════════════════════════════════════════════════

class FileOrganizerHandler(FileSystemEventHandler):
    """Handles file system events for auto-organization."""
    
    def on_created(self, event):
        """Called when a file is created."""
        if event.is_directory:
            return
        
        # Small delay to ensure file is fully written
        time.sleep(1)
        organize_file(event.src_path)


# ══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN
# ══════════════════════════════════════════════════════════════════════════════

def organize_existing_files():
    """Organize all existing files in the watch folder."""
    watch_folder = Path(CONFIG["watch_folder"])
    
    if not watch_folder.exists():
        print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Watch folder not found: {watch_folder}")
        return
    
    print(f"\n{NeonColors.YELLOW}[SCAN]{NeonColors.RESET} Organizing existing files...")
    
    files_organized = 0
    
    # Get all files (not in subdirectories)
    for item in watch_folder.iterdir():
        if item.is_file():
            organize_file(str(item))
            files_organized += 1
    
    print(f"{NeonColors.GREEN}[DONE]{NeonColors.RESET} Organized {files_organized} existing files\n")


def start_monitoring():
    """Start file system monitoring."""
    watch_folder = CONFIG["watch_folder"]
    
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.MAGENTA}🗂️ FILE ORGANIZER - Auto Downloads Manager{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
    
    print(f"{NeonColors.YELLOW}[CONFIG]{NeonColors.RESET} Watch folder: {NeonColors.BOLD}{watch_folder}{NeonColors.RESET}")
    print(f"{NeonColors.YELLOW}[CONFIG]{NeonColors.RESET} Categories: {len(CONFIG['categories'])}")
    print(f"{NeonColors.YELLOW}[CONFIG]{NeonColors.RESET} Log file: {CONFIG['log_file']}\n")
    
    # Check if folder exists
    if not Path(watch_folder).exists():
        print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Folder not found: {watch_folder}")
        print(f"{NeonColors.YELLOW}[INFO]{NeonColors.RESET} Please update CONFIG['watch_folder'] in the script")
        return
    
    # Organize existing files first
    organize_existing_files()
    
    # Start monitoring
    event_handler = FileOrganizerHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_folder, recursive=False)
    observer.start()
    
    print(f"{NeonColors.GREEN}[START]{NeonColors.RESET} Monitoring started")
    print(f"{NeonColors.GREEN}[INFO]{NeonColors.RESET} Press Ctrl+C to stop\n")
    print(f"{NeonColors.CYAN}{'─' * 78}{NeonColors.RESET}\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n\n{NeonColors.YELLOW}[STOP]{NeonColors.RESET} Monitoring stopped by user")
        observer.stop()
    
    observer.join()
    print(f"{NeonColors.GREEN}[EXIT]{NeonColors.RESET} File organizer terminated\n")


# ══════════════════════════════════════════════════════════════════════════════
# 🎯 ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        start_monitoring()
    except Exception as e:
        print(f"\n{NeonColors.RED}[FATAL]{NeonColors.RESET} {e}")
        logging.critical(f"Fatal error: {e}")

