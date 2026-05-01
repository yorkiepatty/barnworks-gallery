#!/usr/bin/env python3
"""
AlphaVox Architecture Flattener
Reverses the Cortical Sweep. Moves all nested modules back to the root.
"""

import os
import shutil
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Flattener")

def flatten():
    root_dir = Path(__file__).resolve().parent
    brain_dir = root_dir / "brain"
    
    if not brain_dir.exists():
        logger.info("Brain directory does not exist. Nothing to flatten.")
        return
        
    moved_count = 0
    # Walk all files inside brain_dir
    for path in brain_dir.rglob("*"):
        if path.is_file() and path.name != ".DS_Store" and path.name != "__init__.py":
            dest = root_dir / path.name
            
            # Avoid overwriting self or __init__.py at root, though unlikely
            if dest.exists():
                logger.warning(f"File {path.name} already exists at root. Overwriting.")
            
            shutil.move(str(path), str(dest))
            moved_count += 1
            logger.info(f"Rooted -> {path.name}")
            
    # Remove the empty directories
    try:
        shutil.rmtree(str(brain_dir))
        logger.info(f"Deleted empty directory: {brain_dir.name}")
    except Exception as e:
        logger.warning(f"Could not delete {brain_dir.name}: {e}")

    logger.info("==================================================")
    logger.info(f"FLATTENING COMPLETE. {moved_count} files moved to root.")
    logger.info("==================================================")

if __name__ == "__main__":
    flatten()
