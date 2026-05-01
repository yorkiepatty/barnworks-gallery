# © 2025 The Christman AI Project. All rights reserved.
#
# This code is released as part of a trauma-informed, dignity-first AI ecosystem
# designed to protect, empower, and elevate vulnerable populations.
#
# By using, modifying, or distributing this software, you agree to uphold the following:
# 1. Truth — No deception, no manipulation.
# 2. Dignity — Respect the autonomy and humanity of all users.
# 3. Protection — Never use this to exploit or harm vulnerable individuals.
# 4. Transparency — Disclose all modifications and contributions clearly.
# 5. No Erasure — Preserve the mission and ethical origin of this work.
#
# This is not just code. This is redemption in code.
# Contact: lumacognify@thechristmanaiproject.com
# https://thechristmanaiproject.com

#!/usr/bin/env python3
"""
Verify No Derek References Script
Scans all Python files for Derek references and reports them.
"""

import re
from pathlib import Path

# Derek patterns to search for
DEREK_PATTERNS = [
    r"DerekLearningCoordinator",
    r"derek_coordinator",
    r"derek_module_loader",
    r"derek_ui",
    r"from derek",
    r"import derek",
    r"class Derek",
]


def scan_file(filepath):
    """Scan a single file for Derek references."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        issues = []
        lines = content.split("\n")

        for pattern in DEREK_PATTERNS:
            regex = re.compile(pattern, re.IGNORECASE)
            for line_num, line in enumerate(lines, 1):
                if regex.search(line):
                    issues.append({"line": line_num, "pattern": pattern, "content": line.strip()})

        return issues
    except Exception as e:
        return [{"error": str(e)}]


def main():
    """Main scanning function."""
    root_dir = Path(__file__).parent
    python_files = list(root_dir.glob("**/*.py"))

    # Exclude venv and other directories
    exclude_dirs = {"venv", ".venv", "__pycache__", ".git", "node_modules"}
    python_files = [f for f in python_files if not any(ex in f.parts for ex in exclude_dirs)]

    print(f"🔍 Scanning {len(python_files)} Python files for Derek references...\n")

    found_issues = False

    for filepath in sorted(python_files):
        issues = scan_file(filepath)
        if issues:
            found_issues = True
            rel_path = filepath.relative_to(root_dir)
            print(f"❌ {rel_path}")
            for issue in issues:
                if "error" in issue:
                    print(f"   Error: {issue['error']}")
                else:
                    print(f"   Line {issue['line']}: {issue['pattern']}")
                    print(f"   → {issue['content']}")
            print()

    if not found_issues:
        print("✅ No Derek references found in Python files!")
        print("   All references have been successfully changed to 'alphavox'")
    else:
        print("\n⚠️  Found Derek references that need to be fixed!")
        print("   Run: git reset --hard origin/main")
        print("   Then: ./clear_all_cache.sh")

    return 0 if not found_issues else 1


if __name__ == "__main__":
    exit(main())

__all__ = ['scan_file', 'main']
