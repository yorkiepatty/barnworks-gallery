#!/usr/bin/env python3
"""Get exact count by testing imports directly"""

import sys
import importlib.util
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def test_import(py_file):
    """Test if a Python file can be imported"""
    try:
        spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
        if spec and spec.loader:
            # Redirect stdout/stderr to suppress output
            import os
            with open(os.devnull, 'w') as devnull:
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = devnull
                sys.stderr = devnull
                try:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    return True, None
                finally:
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr
    except Exception as e:
        return False, str(e)[:50]

def main():
    root_path = Path('.')
    exclude_files = {'brain_orchestrator.py', 'exact_count.py', 'silent_count.py', 'fix_critical.py', 'mass_fix.py', 'final_count.py'}
    
    py_files = [f for f in root_path.glob("*.py") 
                if not f.name.startswith("__") and f.name not in exclude_files]
    
    total = len(py_files)
    loaded = 0
    failed = 0
    failed_list = []
    
    print("Testing module imports...")
    for i, py_file in enumerate(py_files):
        if i % 20 == 0:
            print(f"Progress: {i}/{total}")
        
        success, error = test_import(py_file)
        if success:
            loaded += 1
        else:
            failed += 1
            failed_list.append((py_file.name, error))
    
    success_rate = (loaded / total * 100) if total > 0 else 0
    required_98 = int(total * 0.98)
    gap = required_98 - loaded
    
    print(f"\n=== FINAL EXACT RESULTS ===")
    print(f"Total modules: {total}")
    print(f"Successfully loaded: {loaded}")
    print(f"Failed to load: {failed}")
    print(f"Success rate: {success_rate:.2f}%")
    print(f"Required for 98%: {required_98}")
    print(f"Gap to 98%: {gap}")
    
    if success_rate >= 98.0:
        print("🎉 SUCCESS! ACHIEVED 98%+ SUCCESS RATE!")
    else:
        print(f"❌ STILL UNACCEPTABLE. Need to fix {gap} more modules.")
        print("\nTop 10 failures:")
        for i, (name, error) in enumerate(failed_list[:10], 1):
            print(f"{i:2d}. {name}: {error}")

if __name__ == "__main__":
    main()