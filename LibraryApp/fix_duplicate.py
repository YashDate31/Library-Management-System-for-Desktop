#!/usr/bin/env python3
"""
Script to fix the duplicate actions section in main_new.py
"""

def fix_duplicate_sections():
    with open('main_new.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the duplicate section and remove it
    lines = content.split('\n')
    new_lines = []
    skip_section = False
    skip_count = 0
    
    for i, line in enumerate(lines):
        # Start skipping after we find the students scrollbar pack line and we see Search controls
        if 'students_h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)' in line:
            new_lines.append(line)
            # Check if next few lines contain duplicate search controls
            if i+2 < len(lines) and '# Search controls' in lines[i+2]:
                skip_section = True
                skip_count = 0
                continue
        elif skip_section:
            skip_count += 1
            # Stop skipping when we reach create_books_tab
            if 'def create_books_tab(self):' in line:
                skip_section = False
                new_lines.append(line)
            # Don't add lines while skipping
            continue
        else:
            new_lines.append(line)
    
    # Write the fixed content back
    with open('main_new.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print("Fixed duplicate sections in main_new.py")

if __name__ == "__main__":
    fix_duplicate_sections()