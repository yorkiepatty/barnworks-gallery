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

"""
Quick test to verify Learning Hub is accessible
"""

import os

# Test 1: Can we import the modules?
print("=" * 60)
print("TEST 1: Import Learning Modules")
print("=" * 60)

try:
    from learning_journey import get_learning_journey

    print("✅ learning_journey imported")

    learning_journey = get_learning_journey()
    print("✅ Learning journey instance created")
    print(f"   Topics: {len(learning_journey.topics)}")
    print(f"   Facts: {len(learning_journey.facts)}")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 2: Can we import learning routes?
print("\n" + "=" * 60)
print("TEST 2: Import Learning Routes")
print("=" * 60)

try:
    from learning_routes import learning_bp

    print("✅ routes.learning_routes imported (preferred)")
    print(f"   Blueprint name: {learning_bp.name}")
    print(f"   URL prefix: {learning_bp.url_prefix}")
except Exception as e:
    print(f"⚠️  routes.learning_routes failed: {e}")
    try:
        from learning_routes import learning_bp

        print("✅ learning_routes imported (fallback)")
        print(f"   Blueprint name: {learning_bp.name}")
        print(f"   URL prefix: {learning_bp.url_prefix}")
    except Exception as e2:
        print(f"❌ Both imports failed: {e2}")

# Test 3: Check if routes are registered in app
print("\n" + "=" * 60)
print("TEST 3: Check App Routes")
print("=" * 60)

try:
    from app import app

    learning_routes = []
    for rule in app.url_map.iter_rules():
        if "/learning" in str(rule):
            learning_routes.append(str(rule))

    if learning_routes:
        print(f"✅ Found {len(learning_routes)} learning routes:")
        for route in learning_routes:
            print(f"   {route}")
    else:
        print("❌ No learning routes found in app!")
        print("\n   All registered routes:")
        for rule in list(app.url_map.iter_rules())[:20]:
            print(f"   {rule}")
except Exception as e:
    print(f"❌ Failed to check app routes: {e}")

# Test 4: Check template files
print("\n" + "=" * 60)
print("TEST 4: Check Template Files")
print("=" * 60)

templates_to_check = [
    "templates/learning/hub.html",
    "templates/learning/topics.html",
    "templates/learning/facts.html",
    "templates/learning/journey.html",
]

for template in templates_to_check:
    if os.path.exists(template):
        print(f"✅ {template}")
    else:
        print(f"❌ {template} MISSING")

# Final summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print(
    """
To access Learning Hub:
1. Start the app: python app.py --port 5001
2. Visit: http://localhost:5001/learning
3. Or from menu: Click "Learning Hub" in navigation

If you see errors:
- Check that learning_journey.py exists and is working
- Verify templates/learning/ directory has required HTML files
- Make sure app.py is calling register_learning_routes()
"""
)
