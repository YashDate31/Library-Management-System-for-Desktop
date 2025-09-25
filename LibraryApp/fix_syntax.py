#!/usr/bin/env python3
"""
Script to fix the broken syntax in main_new.py
"""

def fix_students_tab():
    with open('main_new.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the end of the students tab (after scrollbar pack)
    fixed_lines = []
    skip_mode = False
    
    for i, line in enumerate(lines):
        if 'students_h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)' in line:
            fixed_lines.append(line)
            # Skip all lines until we reach the proper books tab start
            skip_mode = True
            continue
            
        if skip_mode:
            # Look for the proper books tab start
            if '"""Create books management tab"""' in line:
                skip_mode = False
                fixed_lines.append(line)
                continue
            # Skip all other lines in between
            continue
        
        fixed_lines.append(line)
    
    # Write the fixed content back
    with open('main_new.py', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("Fixed students tab syntax errors")

if __name__ == "__main__":
    fix_students_tab()