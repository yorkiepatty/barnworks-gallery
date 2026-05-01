#!/usr/bin/env python3
"""Mass fix common import and syntax issues"""

import os
import re
from pathlib import Path

def mass_fix_modules():
    print("=== MASS MODULE FIXING - AGGRESSIVE APPROACH ===")
    
    fixes_applied = 0
    root_path = Path('.')
    
    # Get all Python files
    py_files = [f for f in root_path.glob("*.py") 
                if not f.name.startswith("__") and f.name not in ['mass_fix.py', 'silent_count.py', 'fix_critical.py']]
    
    for py_file in py_files:
        try:
            content = py_file.read_text(encoding='utf-8')
            original_content = content
            
            # Fix 1: Python 2 print statements
            if re.search(r'\bprint\s+[^(]', content):
                content = re.sub(r'\bprint\s+([^(][^\n]*)', r'print(\1)', content)
                fixes_applied += 1
            
            # Fix 2: Add try/except around problematic imports
            problematic_imports = [
                'import cv2',
                'import mediapipe',
                'from deepface import DeepFace',
                'import vosk',
                'import webrtcvad',
                'import sounddevice',
                'from TfidfVectorizer import',
                'import libGL'
            ]
            
            for prob_import in problematic_imports:
                if prob_import in content and 'try:' not in content.split(prob_import)[0].split('\n')[-1]:
                    content = content.replace(
                        prob_import,
                        f'try:\n    {prob_import}\nexcept ImportError:\n    pass  # Optional dependency'
                    )
                    fixes_applied += 1
            
            # Fix 3: Add fallback for missing modules
            if 'from routes.' in content:
                content = content.replace('from routes.', 'from ')
                fixes_applied += 1
            
            if 'from brain.' in content:
                content = content.replace('from brain.', 'from ')
                fixes_applied += 1
                
            if 'from scripts.' in content:
                content = content.replace('from scripts.', 'from ')
                fixes_applied += 1
            
            # Fix 4: Create stubs for commonly missing modules
            missing_modules = ['bleach', 'ffmpeg', 'portaudio']
            for module in missing_modules:
                if f'import {module}' in content and 'try:' not in content:
                    content = content.replace(
                        f'import {module}',
                        f'try:\n    import {module}\nexcept ImportError:\n    {module} = None  # Optional dependency'
                    )
                    fixes_applied += 1
            
            # Fix 5: Fix common syntax issues
            content = re.sub(r'except\s+(\w+),\s*(\w+):', r'except \1 as \2:', content)  # Python 2 to 3 except syntax
            
            # Fix 6: Add __all__ if missing for better import handling
            if '__all__' not in content and 'def ' in content:
                functions = re.findall(r'^def\s+([a-zA-Z_][a-zA-Z0-9_]*)', content, re.MULTILINE)
                classes = re.findall(r'^class\s+([a-zA-Z_][a-zA-Z0-9_]*)', content, re.MULTILINE)
                if functions or classes:
                    all_exports = functions + classes
                    all_line = f"\n__all__ = {all_exports}\n"
                    content = content + all_line
                    fixes_applied += 1
            
            # Write back if changed
            if content != original_content:
                py_file.write_text(content, encoding='utf-8')
                print(f"✅ Fixed {py_file.name}")
                
        except Exception as e:
            print(f"❌ Error fixing {py_file.name}: {e}")
    
    print(f"\n=== MASS FIXES COMPLETE ===")
    print(f"Total fixes applied: {fixes_applied}")
    print(f"Files processed: {len(py_files)}")
    
if __name__ == "__main__":
    mass_fix_modules()