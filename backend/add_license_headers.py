#!/usr/bin/env python3
"""
Script to add The Christman AI Project license header to all Python files
"""

import glob

LICENSE_HEADER = """# © 2025 The Christman AI Project. All rights reserved.
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

"""


def has_license_header(file_path):
    """Check if file already has our license header"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return "© 2025 The Christman AI Project" in content
    except:
        return False


def add_license_to_file(file_path):
    """Add license header to the top of a Python file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Skip if already has license
        if has_license_header(file_path):
            print(f"SKIP: {file_path} (already has license)")
            return False

        # Add license header at the top
        new_content = LICENSE_HEADER + content

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅ Added license to: {file_path}")
        return True

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False


def main():
    """Add license headers to all Python files"""
    python_files = glob.glob("**/*.py", recursive=True)

    print(f"Found {len(python_files)} Python files")
    print("Adding license headers...\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0

    for file_path in python_files:
        # Skip this script itself
        if file_path.endswith("add_license_headers.py"):
            continue

        if has_license_header(file_path):
            print(f"SKIP: {file_path}")
            skipped_count += 1
        else:
            if add_license_to_file(file_path):
                updated_count += 1
            else:
                error_count += 1

    print("\n=== SUMMARY ===")
    print(f"Updated: {updated_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")
    print(f"Total: {len(python_files)}")


if __name__ == "__main__":
    main()

__all__ = ['has_license_header', 'add_license_to_file', 'main']
