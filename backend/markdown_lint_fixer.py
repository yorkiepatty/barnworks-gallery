#!/usr/bin/env python3
"""
Markdown Lint Fixer for AlphaVox
Fixes common markdown issues to reduce explorer paranoia
"""

import re
from pathlib import Path

class MarkdownLintFixer:
    """Fix common markdown lint issues"""
    
    def __init__(self):
        self.fixes_applied = 0
    
    def fix_markdown_file(self, file_path):
        """Fix all markdown issues in a file"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix MD022: Blank lines around headings
            content = re.sub(r'^(#+\s+.*?)$', r'\n\1\n', content, flags=re.MULTILINE)
            
            # Fix MD032: Blank lines around lists
            content = re.sub(r'^([^-*1-9\n].*)\n([-*]|\d+\.)', r'\1\n\n\2', content, flags=re.MULTILINE)
            content = re.sub(r'^([-*].*|\d+\..*)\n([^-*1-9\n])', r'\1\n\n\2', content, flags=re.MULTILINE)
            
            # Fix MD036: No emphasis as heading - convert *text* at start of line to ## text
            content = re.sub(r'^\*([^*]+)\*$', r'## \1', content, flags=re.MULTILINE)
            
            # Fix MD026: Remove trailing punctuation from headings
            content = re.sub(r'^(#+\s+.*?)[:.]$', r'\1', content, flags=re.MULTILINE)
            
            # Fix MD034: Bare URLs - wrap in <>
            content = re.sub(r'(?<![\[\(<])(https?://[^\s\)>\]]+)(?![\]\)>])', r'<\1>', content)
            
            # Fix MD047: Single trailing newline
            content = content.rstrip() + '\n'
            
            # Remove excessive blank lines
            content = re.sub(r'\n{3,}', '\n\n', content)
            
            # Remove blank lines at start
            content = content.lstrip('\n')
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.fixes_applied += 1
                print(f"✅ Fixed: {file_path}")
            else:
                print(f"   Clean: {file_path}")
                
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")
    
    def fix_all_markdown(self, root_path):
        """Fix all markdown files in directory"""
        
        root = Path(root_path)
        markdown_files = list(root.glob('**/*.md'))
        
        print(f"🔧 Fixing {len(markdown_files)} markdown files...")
        print("=" * 60)
        
        for md_file in markdown_files:
            self.fix_markdown_file(md_file)
        
        print("=" * 60)
        print(f"✅ Applied {self.fixes_applied} markdown fixes")
        print("🧠 AlphaVox Explorer Paranoia Reduced!")
        
if __name__ == "__main__":
    fixer = MarkdownLintFixer()
    fixer.fix_all_markdown("/Users/EverettN/ALPHAVOXWAKESUP")
    
    print("\n🎯 Markdown lint fixing complete!")
    print("   Explorer should be much cleaner now.")
__all__ = ['MarkdownLintFixer']
