#!/usr/bin/env python3
"""
Quick Email URL Fixer for AlphaVox
Fixes bare email addresses in markdown files
"""

import re
from pathlib import Path

def fix_email_urls(file_path):
    """Fix bare email addresses by wrapping them in angle brackets"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix bare email addresses
        email_pattern = r'(?<!<)(lumacognify@thechristmanaiproject\.com)(?!>)'
        content = re.sub(email_pattern, r'<\1>', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed email URLs in: {file_path}")
            return True
        else:
            print(f"   Clean: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def fix_all_email_urls():
    """Fix email URLs in all markdown files"""
    
    root = Path("/Users/EverettN/ALPHAVOXWAKESUP")
    
    # Key files with email issues
    files_to_fix = [
        "documentation/README.md",
        "configuration/README.md", 
        "frontend/README.md"
    ]
    
    fixes_applied = 0
    
    for file_path in files_to_fix:
        full_path = root / file_path
        if full_path.exists():
            if fix_email_urls(full_path):
                fixes_applied += 1
    
    print(f"\n✅ Fixed {fixes_applied} files with email URL issues")
    print("🧠 Explorer paranoia further reduced!")

if __name__ == "__main__":
    fix_all_email_urls()
__all__ = ['fix_email_urls', 'fix_all_email_urls']
