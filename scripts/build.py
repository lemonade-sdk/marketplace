#!/usr/bin/env python3
"""
Build script for the Lemonade Marketplace.
Combines individual app.json files into a single apps.json file.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Repository base URL for logo assets
REPO_BASE_URL = "https://raw.githubusercontent.com/lemonade-sdk/marketplace/main"

# Category definitions
CATEGORIES = [
    {"id": "chat", "label": "Chat"},
    {"id": "code", "label": "Code"},
    {"id": "creative", "label": "Creative"},
    {"id": "automation", "label": "Automation"},
    {"id": "app", "label": "Apps"},
]

# Required fields in app.json
REQUIRED_FIELDS = ["id", "name", "description", "category", "links", "date_added"]


def validate_app(app_data: dict, app_dir: str) -> list[str]:
    """Validate an app.json file and return list of errors."""
    errors = []
    
    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in app_data:
            errors.append(f"Missing required field: {field}")
    
    # Validate types
    if "category" in app_data and not isinstance(app_data["category"], list):
        errors.append("'category' must be a list")
    
    if "date_added" in app_data:
        # Validate date format (YYYY-MM-DD)
        try:
            datetime.strptime(app_data["date_added"], "%Y-%m-%d")
        except ValueError:
            errors.append("'date_added' must be in YYYY-MM-DD format")
    
    if "links" in app_data:
        if not isinstance(app_data["links"], dict):
            errors.append("'links' must be an object")
        elif "app" not in app_data["links"]:
            errors.append("'links.app' is required")
    
    return errors


def find_logo(app_dir: Path) -> str | None:
    """Find logo file in app directory. Returns relative path or None."""
    for ext in [".png", ".jpg", ".jpeg", ".svg", ".webp"]:
        logo_path = app_dir / f"logo{ext}"
        if logo_path.exists():
            return f"logo{ext}"
    return None


def load_pinned_apps(repo_root: Path) -> set[str]:
    """Load the list of pinned app IDs from pinned.json."""
    pinned_path = repo_root / "pinned.json"
    if not pinned_path.exists():
        print(f"[WARN] No pinned.json found at {pinned_path}")
        return set()
    
    try:
        with open(pinned_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data.get("pinned", []))
    except (json.JSONDecodeError, KeyError) as e:
        print(f"[WARN] Error reading pinned.json: {e}")
        return set()


def build_apps_json(apps_dir: Path, output_path: Path, pinned_ids: set[str]) -> bool:
    """Build the apps.json file from individual app.json files."""
    apps = []
    errors = []
    
    # Iterate through app directories
    for app_dir in sorted(apps_dir.iterdir()):
        if not app_dir.is_dir():
            continue
        
        app_json_path = app_dir / "app.json"
        if not app_json_path.exists():
            print(f"[WARN] No app.json found in {app_dir.name}")
            continue
        
        try:
            with open(app_json_path, "r", encoding="utf-8") as f:
                app_data = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"{app_dir.name}: Invalid JSON - {e}")
            continue
        
        # Validate
        validation_errors = validate_app(app_data, str(app_dir))
        if validation_errors:
            for err in validation_errors:
                errors.append(f"{app_dir.name}: {err}")
            continue
        
        # Find logo
        logo_file = find_logo(app_dir)
        if logo_file:
            app_data["logo"] = f"{REPO_BASE_URL}/apps/{app_dir.name}/{logo_file}"
        else:
            # No logo found - use a placeholder
            app_data["logo"] = f"{REPO_BASE_URL}/assets/placeholder.png"
            print(f"[WARN] No logo found for {app_dir.name}")
        
        # Add derived "pinned" field based on presence in pinned.json
        app_data["pinned"] = app_data["id"] in pinned_ids
        
        apps.append(app_data)
    
    # Report errors
    if errors:
        print("\n[ERROR] Validation errors found:")
        for err in errors:
            print(f"   - {err}")
        return False
    
    # Sort: pinned apps first, then by date_added (newest first), then alphabetically by name
    def sort_key(app):
        is_pinned = 0 if app.get("pinned") else 1
        # Parse date for sorting (newer dates should come first, so negate)
        date_str = app.get("date_added", "1970-01-01")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            # Invert date for descending order (newer first)
            date_sort = -date.timestamp()
        except ValueError:
            date_sort = 0
        name = app.get("name", "").lower()
        return (is_pinned, date_sort, name)
    
    apps.sort(key=sort_key)
    
    # Build output
    output = {
        "version": "1.0",
        "generated": datetime.now(timezone.utc).isoformat(),
        "apps": apps,
        "categories": CATEGORIES,
    }
    
    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Successfully generated {output_path}")
    print(f"   - {len(apps)} apps")
    print(f"   - {len([a for a in apps if a.get('pinned')])} pinned")
    
    return True


def main():
    # Determine paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    apps_dir = repo_root / "apps"
    output_path = repo_root / "apps.json"
    
    if not apps_dir.exists():
        print(f"[ERROR] Apps directory not found at {apps_dir}")
        sys.exit(1)
    
    print(f"[BUILD] Building apps.json from {apps_dir}")
    
    # Load pinned apps
    pinned_ids = load_pinned_apps(repo_root)
    print(f"[INFO] Loaded {len(pinned_ids)} pinned apps")
    
    success = build_apps_json(apps_dir, output_path, pinned_ids)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
