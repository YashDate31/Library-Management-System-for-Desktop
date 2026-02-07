#!/usr/bin/env python3
"""Fix Unicode emoji characters in print statements to prevent console encoding issues"""
import re
import os

def fix_unicode_in_file(filepath):
    """Replace emoji with ASCII equivalents in print statements"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Replace print statements with emoji - keep only print statements, not string UI labels
    # Only replace within print() calls
    replacements = [
        (r'print\(f?"([^"]*?)✅([^"]*)"\)', r'print(f"\1[OK]\2")'),
        (r'print\(f?"([^"]*?)❌([^"]*)"\)', r'print(f"\1[ERROR]\2")'),
        (r'print\(f?"([^"]*?)⚠️([^"]*)"\)', r'print(f"\1[WARNING]\2")'),
        (r'print\(f?"([^"]*?)📊([^"]*)"\)', r'print(f"\1[STATS]\2")'),
        (r'print\(f?"([^"]*?)✨([^"]*)"\)', r'print(f"\1[DONE]\2")'),
        (r'print\(f?"([^"]*?)\\u2705([^"]*)"\)', r'print(f"\1[OK]\2")'),
        (r'print\(f?"([^"]*?)\\u26a0\\ufe0f([^"]*)"\)', r'print(f"\1[WARNING]\2")'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Also replace in f-strings with print - more comprehensive
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if 'print(' in line and ('✅' in line or '❌' in line or '⚠️' in line or '📊' in line or '✨' in line or '\\u' in line):
            # Replace emoji in this line
            line = line.replace('✅', '[OK]').replace('❌', '[ERROR]').replace('⚠️', '[WARNING]').replace('📊', '[STATS]').replace('✨', '[DONE]')
            line = line.replace('\\u2705', '[OK]').replace('\\u26a0\\ufe0f', '[WARNING]').replace('\\u274c', '[ERROR]')
        new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] Fixed Unicode in {filepath}")
        return True
    return False

# Fix all Python files
py_files = [
    'main.py',
    'database.py',
    'sync_manager.py',
    'create_demo_data.py',
    'Web-Extension/student_portal.py',
]

for py_file in py_files:
    filepath = os.path.join(os.path.dirname(__file__), py_file)
    if os.path.exists(filepath):
        fix_unicode_in_file(filepath)
        print(f"[OK] Processed {py_file}")

print("[OK] Unicode fixes completed!")
