#!/usr/bin/env python3
"""Get exact brain module counts without logs"""

import sys
import os
import logging
from pathlib import Path
import importlib.util

# Suppress ALL logging
logging.disable(logging.CRITICAL)

# Add root path
root_path = str(Path(__file__).parent)
if root_path not in sys.path:
    sys.path.insert(0, root_path)

class BrainModule:
    def __init__(self, module_path: str, module_name: str):
        self.module_path = module_path
        self.module_name = module_name
        self.loaded = False
        self.error = None
        
    def load(self):
        try:
            spec = importlib.util.spec_from_file_location(self.module_name, self.module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.loaded = True
        except Exception as e:
            self.error = str(e)

def count_modules():
    modules = {}
    loaded_count = 0
    total_count = 0
    failed_modules = []
    
    root_path = Path(__file__).parent
    
    for py_file in root_path.glob("*.py"):
        if py_file.name.startswith("__") or py_file.name in ["brain_orchestrator.py", "exact_count.py"]:
            continue
        
        module_key = py_file.stem
        module = BrainModule(str(py_file), py_file.stem)
        modules[module_key] = module
        total_count += 1
        
        # Try to load the module
        module.load()
        if module.loaded:
            loaded_count += 1
        else:
            failed_modules.append((module_key, module.error))
    
    success_rate = (loaded_count / total_count * 100) if total_count > 0 else 0
    required_98_percent = int(total_count * 0.98)
    
    print("=== EXACT BRAIN MODULE STATISTICS ===")
    print(f"Total modules: {total_count}")
    print(f"Loaded modules: {loaded_count}")
    print(f"Failed modules: {total_count - loaded_count}")
    print(f"Success rate: {success_rate:.2f}%")
    print(f"Required for 98%: {required_98_percent} modules")
    print(f"Gap to 98%: {required_98_percent - loaded_count} modules need fixing")
    print()
    
    if failed_modules:
        print("=== FAILED MODULES (NEED FIXING) ===")
        for i, (name, error) in enumerate(failed_modules[:20], 1):  # Show first 20
            print(f"{i:2d}. {name}: {error[:80]}...")
        if len(failed_modules) > 20:
            print(f"    ... and {len(failed_modules) - 20} more")
    
    return {
        "total_modules": total_count,
        "loaded_modules": loaded_count,
        "success_rate": success_rate,
        "failed_modules": failed_modules
    }

if __name__ == "__main__":
    count_modules()
__all__ = ['count_modules', 'BrainModule']
