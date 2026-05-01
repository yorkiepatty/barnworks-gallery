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
Compare Mac vs Codespace environments to identify Learning Hub issues.
This shows what changed between when it was working and now.
"""

import json
import os
from datetime import datetime

print("=" * 80)
print("ENVIRONMENT COMPARISON - Learning Hub Debugging")
print("=" * 80)
print(f"Generated: {datetime.now()}")
print()

# 1. CHECK DATA FILES
print("1. DATA FILES CHECK:")
print("-" * 80)

data_files = {
    "Topics": "data/knowledge/topics.json",
    "Facts": "data/knowledge/facts.json",
    "Knowledge Graph": "data/knowledge_graph.json",
    "Learning Log": "data/knowledge/learning_log.json",
}

for name, path in data_files.items():
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    count = len(data)
                elif isinstance(data, dict):
                    count = len(data.keys())
                else:
                    count = 1
                print(f"✅ {name:<20} {path:<40} ({count} items)")
            except json.JSONDecodeError:
                print(f"⚠️  {name:<20} {path:<40} (JSON ERROR)")
    else:
        print(f"❌ {name:<20} {path:<40} (MISSING)")

print()

# 2. CHECK ROUTE FILES
print("2. ROUTE FILES CHECK:")
print("-" * 80)

route_files = [
    "learning_routes.py",
    "routes/learning_routes.py",
]

for route_file in route_files:
    if os.path.exists(route_file):
        size = os.path.getsize(route_file)

        # Check for specific route definitions
        with open(route_file, "r") as f:
            content = f.read()
            routes_found = []
            route_patterns = [
                ('@learning_bp.route("/learning"', "/learning"),
                ('@learning_bp.route("/topics"', "/topics"),
                ('@learning_bp.route("/facts"', "/facts"),
                ('@learning_bp.route("/journey"', "/journey"),
                ('@learning_bp.route("/graph"', "/graph"),
            ]

            for pattern, route_name in route_patterns:
                if pattern in content:
                    routes_found.append(route_name)

        print(f"✅ {route_file:<40} ({size:,} bytes)")
        print(f"   Routes defined: {', '.join(routes_found)}")
    else:
        print(f"❌ {route_file:<40} (MISSING)")

print()

# 3. CHECK TEMPLATES
print("3. TEMPLATE FILES CHECK:")
print("-" * 80)

templates = [
    "templates/learning/hub.html",
    "templates/learning/topics.html",
    "templates/learning/facts.html",
    "templates/learning/journey.html",
    "templates/learning/graph.html",
    "templates/learning/topic_detail.html",
    "templates/learning/fact_detail.html",
]

for template in templates:
    if os.path.exists(template):
        size = os.path.getsize(template)
        print(f"✅ {template:<50} ({size:,} bytes)")
    else:
        print(f"❌ {template:<50} (MISSING)")

print()

# 4. CHECK PYTHON MODULES
print("4. PYTHON MODULE IMPORTS:")
print("-" * 80)

modules_to_test = [
    ("learning_journey", "LearningJourney"),
    ("learning_analytics", "LearningAnalytics"),
    ("knowledge_engine", "KnowledgeEngine"),
    ("learning_service", "LearningService"),
]

working_modules = []
failed_modules = []

for module_name, class_name in modules_to_test:
    try:
        module = __import__(module_name)
        if hasattr(module, class_name):
            print(f"✅ {module_name:<30} (has {class_name})")
            working_modules.append(module_name)
        else:
            print(f"⚠️  {module_name:<30} (missing {class_name})")
            working_modules.append(module_name)
    except Exception as e:
        print(f"❌ {module_name:<30} (ERROR: {str(e)[:50]})")
        failed_modules.append((module_name, str(e)))

print()

# 5. CHECK APP.PY INTEGRATION
print("5. APP.PY INTEGRATION CHECK:")
print("-" * 80)

if os.path.exists("app.py"):
    with open("app.py", "r") as f:
        app_content = f.read()

    checks = [
        (
            "learning_routes import",
            "from learning_routes import" in app_content or "import learning_routes" in app_content,
        ),
        ("register_learning_routes", "register_learning_routes" in app_content),
        ("learning_bp", "learning_bp" in app_content),
        (
            "/learning route",
            '@app.route("/learning")' in app_content or "@app.route('/learning')" in app_content,
        ),
    ]

    for check_name, found in checks:
        status = "✅" if found else "❌"
        print(f"{status} {check_name}")
else:
    print("❌ app.py not found")

print()

# 6. CHECK REQUIREMENTS
print("6. REQUIREMENTS CHECK:")
print("-" * 80)

if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r") as f:
        requirements = f.read()

    critical_packages = ["Flask", "flask", "jinja2", "Jinja2"]

    for pkg in critical_packages:
        if pkg in requirements:
            print(f"✅ {pkg} listed in requirements.txt")
        else:
            print(f"⚠️  {pkg} NOT in requirements.txt")
else:
    print("❌ requirements.txt not found")

print()

# 7. GENERATE DIAGNOSTIC QUESTIONS
print("7. DIAGNOSTIC QUESTIONS FOR MAC:")
print("-" * 80)
print()
print("Run these commands on your Mac and share the output:")
print()
print("1. Check if routes file imports successfully:")
print("   python -c \"from learning_routes import learning_bp; print('SUCCESS')\"\n")
print("2. Check Learning Journey module:")
print("   python -c \"from learning_journey import LearningJourney; print('SUCCESS')\"\n")
print("3. Check Flask is installed:")
print('   python -c "import flask; print(flask.__version__)"\n')
print("4. Check which Python is running:")
print("   which python\n")
print("5. List installed packages:")
print("   pip list | grep -i flask\n")
print("6. Check if venv is activated:")
print("   echo $VIRTUAL_ENV\n")
print("7. Start app with verbose logging:")
print("   python app.py --port 5001 2>&1 | grep -i learning\n")

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)

if failed_modules:
    print("\n❌ CRITICAL: The following modules failed to import:")
    for mod, error in failed_modules:
        print(f"   - {mod}: {error[:60]}")
    print("\nThis is likely why Learning Hub isn't loading on your Mac.")
else:
    print("\n✅ All core modules imported successfully!")
    print("\nIf Learning Hub still shows 404 on your Mac, the issue is likely:")
    print("  1. Routes aren't being registered in app.py startup")
    print("  2. Blueprint registration is failing silently")
    print("  3. Different Flask version behavior")

print()
print("Next step: Run the diagnostic questions above on your Mac")
print()
