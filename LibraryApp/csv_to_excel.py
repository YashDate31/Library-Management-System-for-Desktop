import pandas as pd

# Read CSV files and save as Excel
students_df = pd.read_csv('sample_students.csv')
books_df = pd.read_csv('sample_books.csv')

students_df.to_excel('sample_students.xlsx', index=False)
books_df.to_excel('sample_books.xlsx', index=False)

print("✅ Created sample_students.xlsx")
print("✅ Created sample_books.xlsx")
print("\nThese files can be used to test the Excel import functionality!")