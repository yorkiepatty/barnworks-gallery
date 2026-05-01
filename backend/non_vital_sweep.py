#!/usr/bin/env python3
"""
AlphaVox Non-Vital Organizer
Sweeps auxiliary files (.md, .json, archives) into organized folders.
Crucially enforces that NO .py, .db, or operational files leave root.
"""

import os
import shutil
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("NonVitalSweep")

def organize():
    root = Path(__file__).resolve().parent
    
    # Define targets
    targets = {
        ".md": root / "documentation" / "markdown",
        ".txt": root / "documentation" / "text",
        ".json": root / "data" / "json",
        ".tar.gz": root / "archive",
        ".zip": root / "archive",
        ".sh": root / "scripts"
    }
    
    # Ensure targets exist
    for dir_path in targets.values():
        dir_path.mkdir(parents=True, exist_ok=True)
        
    protected_files = {
        "README.md",
        "requirements.txt",
        "requirements-fixed.txt",
        "requirements-production.txt",
        ".env",
        ".gitignore",
        "flatten_repo.py",
        "non_vital_sweep.py",
        "voice_cortex_config.json", # Actively used by voice_cortex.py at root
        "alphavox_knowledge_base.json" # Actively used
    }
    
    moved_count = 0
    forbidden_extensions = {".py", ".db", ".pyc"}
    
    for item in root.iterdir():
        if not item.is_file():
            continue
            
        if item.name in protected_files:
            continue
            
        # Hard lock against vital operational files
        if item.suffix in forbidden_extensions:
            continue
            
        # Match extensions and move
        moved = False
        for ext, dest_dir in targets.items():
            if item.name.endswith(ext):
                dest = dest_dir / item.name
                shutil.move(str(item), str(dest))
                logger.info(f"Swept {item.name} -> {dest_dir.name}/")
                moved_count += 1
                moved = True
                break
                
        if not moved and item.suffix not in forbidden_extensions and not item.name.startswith("."):
            logger.debug(f"Left untouched: {item.name}")

    logger.info("==================================================")
    logger.info(f"NON-VITAL SWEEP COMPLETE. {moved_count} files organized.")
    logger.info("==================================================")

if __name__ == "__main__":
    organize()
