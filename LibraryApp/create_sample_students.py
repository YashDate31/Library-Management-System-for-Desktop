#!/usr/bin/env python3
import pandas as pd

# Sample student data for import testing
students_data = [
    {
        'enrollment_no': '24210270287',
        'name': 'MULE KAVERI SHIVRAJ',
        'email': 'kaveri.mule@email.com',
        'phone': '9876543210',
        'department': 'Computer',
        'year': '2nd'
    },
    {
        'enrollment_no': '23210270221',
        'name': 'POKHARKAR ARYAN NITIN',
        'email': 'aryan.pokharkar@email.com', 
        'phone': '9876543211',
        'department': 'Computer',
        'year': '3rd'
    },
    {
        'enrollment_no': '24210270230',
        'name': 'SHARMA PRIYA RAJESH',
        'email': 'priya.sharma@email.com',
        'phone': '9876543212', 
        'department': 'Computer',
        'year': '2nd'
    },
    {
        'enrollment_no': '23210270225',
        'name': 'PATIL RAHUL KUMAR',
        'email': 'rahul.patil@email.com',
        'phone': '9876543213',
        'department': 'Computer', 
        'year': '3rd'
    },
    {
        'enrollment_no': '24210270231',
        'name': 'JOSHI ANITA SURESH',
        'email': 'anita.joshi@email.com',
        'phone': '9876543214',
        'department': 'Computer',
        'year': '2nd'
    }
]

# Create DataFrame and save to Excel
df = pd.DataFrame(students_data)
output_file = 'sample_students_import.xlsx'
df.to_excel(output_file, index=False)
print(f"Sample Excel file created: {output_file}")
print(f"Contains {len(students_data)} student records")
print("Columns:", list(df.columns))