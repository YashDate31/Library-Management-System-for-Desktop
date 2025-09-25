#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Test Excel import functionality

import pandas as pd
import os

def test_excel_functionality():
    print("Testing Excel import functionality...")
    
    # Check if sample Excel files exist
    excel_files = [
        "sample_students.xlsx", 
        "sample_books.xlsx",
        "sample_students_import.xlsx"
    ]
    
    for file in excel_files:
        if os.path.exists(file):
            print(f"✅ Found {file}")
            try:
                df = pd.read_excel(file)
                print(f"   - Rows: {len(df)}")
                print(f"   - Columns: {list(df.columns)}")
                if not df.empty:
                    print(f"   - First row: {dict(df.iloc[0])}")
            except Exception as e:
                print(f"   ❌ Error reading {file}: {e}")
        else:
            print(f"❌ Missing {file}")
    
    # Test basic pandas functionality
    try:
        test_data = {
            'enrollment_no': ['24210270230', '24210270231'],
            'name': ['Test Student 1', 'Test Student 2'],
            'email': ['test1@example.com', 'test2@example.com'],
            'phone': ['1234567890', '0987654321'],
            'department': ['Computer', 'Computer'],
            'year': ['1st Year', '2nd Year']
        }
        df = pd.DataFrame(test_data)
        print(f"\n✅ Pandas DataFrame creation successful")
        print(f"   - Shape: {df.shape}")
        print(f"   - Columns: {list(df.columns)}")
        
        # Test column normalization (what the import functions do)
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        print(f"   - Normalized columns: {list(df.columns)}")
        
    except Exception as e:
        print(f"❌ Pandas test failed: {e}")

if __name__ == "__main__":
    test_excel_functionality()