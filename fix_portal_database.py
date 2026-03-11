#!/usr/bin/env python3
"""
Quick fix script to ensure portal uses local database
"""

import os
import sys

print("=" * 70)
print("PORTAL DATABASE FIX - Force Local Mode")
print("=" * 70)
print()

# Check .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(env_path):
    print(f"[1] Found .env file: {env_path}")
    
    # Read current content
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Check if PORTAL_FORCE_LOCAL exists
    if 'PORTAL_FORCE_LOCAL' in content:
        print("[2] ✅ PORTAL_FORCE_LOCAL already set in .env")
    else:
        print("[2] ⚠️  PORTAL_FORCE_LOCAL not found in .env")
        print("[3] Adding PORTAL_FORCE_LOCAL=true to .env...")
        
        # Add the setting
        if not content.endswith('\n'):
            content += '\n'
        content += '\n# Portal Configuration - Force LOCAL database\n'
        content += 'PORTAL_FORCE_LOCAL=true\n'
        
        with open(env_path, 'w') as f:
            f.write(content)
        
        print("[4] ✅ Added PORTAL_FORCE_LOCAL=true to .env")
else:
    print(f"[1] ⚠️  .env file not found at {env_path}")
    print("[2] Creating .env file with PORTAL_FORCE_LOCAL=true...")
    
    with open(env_path, 'w') as f:
        f.write('# Portal Configuration - Force LOCAL database\n')
        f.write('PORTAL_FORCE_LOCAL=true\n')
    
    print("[3] ✅ Created .env with PORTAL_FORCE_LOCAL=true")

print()
print("=" * 70)
print("VERIFICATION")
print("=" * 70)
print()

# Load and verify
try:
    from dotenv import load_dotenv
    load_dotenv(env_path)
    
    force_local = os.getenv('PORTAL_FORCE_LOCAL', '')
    print(f"PORTAL_FORCE_LOCAL = '{force_local}'")
    
    if force_local.lower() in ('true', '1', 'yes'):
        print()
        print("✅ SUCCESS! Portal will now use LOCAL database")
        print()
        print("NEXT STEPS:")
        print("1. RESTART the application completely")
        print("2. Start the Student Portal")
        print("3. Add a book from the librarian side")
        print("4. Check the portal - book should appear immediately!")
    else:
        print()
        print("⚠️  WARNING: PORTAL_FORCE_LOCAL is not set to 'true'")
        print(f"   Current value: '{force_local}'")
except Exception as e:
    print(f"⚠️  Error loading .env: {e}")

print()
print("=" * 70)
