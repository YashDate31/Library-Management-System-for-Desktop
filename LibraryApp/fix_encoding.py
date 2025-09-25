#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script to fix the corrupted developer emoji in main.py

import os

def fix_developer_emoji():
    """Fix the corrupted developer emoji in main.py"""
    file_path = "main.py"
    
    # Read the file with proper encoding
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Replace the corrupted emoji with the correct one
    # Find the corrupted pattern and replace it
    old_pattern = '"�‍💻 Developer"'
    new_pattern = '"👨‍💻 Developer"'
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        print(f"Found and fixed corrupted developer emoji")
        
        # Write back with proper encoding
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Developer emoji fixed successfully!")
    else:
        print("❌ Corrupted emoji pattern not found")
        
        # Show what we actually have
        import re
        developer_lines = []
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'Developer' in line and 'text=' in line:
                developer_lines.append(f"Line {i}: {line.strip()}")
        
        if developer_lines:
            print("Found these Developer text lines:")
            for line in developer_lines:
                print(f"  {line}")

if __name__ == "__main__":
    fix_developer_emoji()