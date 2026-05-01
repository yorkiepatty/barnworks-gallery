#!/usr/bin/env python3
"""
Complete route diagnostic tool - see what routes are actually registered
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def diagnose_routes():
    """Show all registered routes in the Flask app"""
    print("=== ALPHAVOX ROUTE DIAGNOSIS ===")

    # We need to run the full app.py to get all routes registered
    # Import everything the way app.py does it
    print("Importing full app.py module to get complete route registration...")
    import app as app_module  # This will run the full app.py and register all routes

    # Get the Flask app object
    flask_app = app_module.app

    print(f"App created successfully: {flask_app}")
    print(f"App name: {flask_app.name}")
    print(f"App config: {dict(flask_app.config)}")
    print()

    # Show all registered routes
    print("=== REGISTERED ROUTES ===")
    routes = []
    for rule in flask_app.url_map.iter_rules():
        routes.append(
            {
                "endpoint": rule.endpoint,
                "methods": list(rule.methods),
                "rule": rule.rule,
            }
        )

    # Sort by rule for easier reading
    routes.sort(key=lambda x: x["rule"])

    for route in routes:
        methods = [m for m in route["methods"] if m not in ["HEAD", "OPTIONS"]]
        print(f"{route['rule']:30} -> {route['endpoint']:30} [{', '.join(methods)}]")

    print(f"\nTotal routes registered: {len(routes)}")

    # Check specifically for missing routes
    print("\n=== CHECKING FOR EXPECTED ROUTES ===")
    expected_routes = [
        "/learning",
        "/learning/",
        "/learning/hub",
        "/caregiver",
        "/caregiver/",
        "/api/behavior",
        "/api/learning",
        "/voice",
        "/voice/",
    ]

    actual_rules = [rule.rule for rule in flask_app.url_map.iter_rules()]

    for expected in expected_routes:
        if expected in actual_rules:
            print(f"✓ {expected} - FOUND")
        else:
            print(f"✗ {expected} - MISSING")

    # Show blueprints
    print("\n=== REGISTERED BLUEPRINTS ===")
    for name, blueprint in flask_app.blueprints.items():
        print(f"Blueprint: {name} -> {blueprint}")
        print(f"  URL prefix: {blueprint.url_prefix}")
        print(f"  Static folder: {blueprint.static_folder}")
        print(f"  Template folder: {blueprint.template_folder}")
        print()


if __name__ == "__main__":
    try:
        diagnose_routes()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()

__all__ = ['diagnose_routes']
