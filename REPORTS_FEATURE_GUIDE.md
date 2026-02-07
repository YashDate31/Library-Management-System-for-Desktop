# 📄 Reports Feature Guide

## Overview
The Reports Center is a comprehensive reporting system integrated into the Library Management System. It provides powerful data export capabilities with filtering options in both **Excel** and **PDF** formats.

## Location
The Reports tab is located between the **Analysis** tab and the **Admin** tab in the main application interface.

## Features

### 1. **Students Report** 👥
- **Description**: Complete list of all registered students with their details
- **Data Included**:
  - Enrollment Number
  - Name
  - Email
  - Phone
  - Year (1st Year, 2nd Year, 3rd Year, Pass Out)
  - Registration Date
- **Filters Available**:
  - Date Range (From-To)
  - Year (All, 1st Year, 2nd Year, 3rd Year, Pass Out)

### 2. **Books Report** 📚
- **Description**: Comprehensive catalog of all books in the library
- **Data Included**:
  - Book ID
  - Title
  - Author
  - Category
  - Status (Available/Borrowed)
  - Condition
  - Added Date
- **Filters Available**:
  - Date Range (From-To)
  - Category (All, Technology, Textbook, Research)

### 3. **Transactions Report** 📖
- **Description**: Detailed transaction history of all book loans
- **Data Included**:
  - Enrollment Number
  - Student Name
  - Book ID
  - Book Title
  - Issue Date
  - Due Date
  - Return Date
  - Status (Active/Returned/Overdue)
  - Fine Amount
- **Filters Available**:
  - Date Range (From-To)
  - Type (All, Active, Returned, Overdue)

### 4. **Overdue Books Report** ⚠️
- **Description**: List of all books that are currently overdue
- **Data Included**:
  - Enrollment Number
  - Student Name
  - Phone
  - Book ID
  - Book Title
  - Issue Date
  - Due Date
  - Days Overdue
  - Fine Amount (automatically calculated)
- **Filters Available**:
  - Date Range (From-To)

### 5. **Promotion History** ⬆️
- **Description**: Historical record of all student year promotions
- **Data Included**:
  - Date
  - Action Description
  - Students Affected
  - From Year
  - To Year
  - Details (Letter Number, Academic Year)
- **Filters Available**:
  - Date Range (From-To)

### 6. **Admin Activity Log** 📋
- **Description**: Comprehensive log of all administrative actions
- **Data Included**:
  - Timestamp
  - Action Type
  - Details
  - Admin User
- **Filters Available**:
  - Date Range (From-To)
- **Logged Activities**:
  - Student additions and deletions
  - Book additions and deletions
  - Book issue and return operations
  - Student year promotions
  - Report exports
  - System configuration changes

## Export Formats

### Excel Export (.xlsx)
- Professional formatting with headers and metadata
- Color-coded headers
- Auto-sized columns
- Includes generation timestamp
- Shows applied filters
- Total record count
- Can be opened with Microsoft Excel, LibreOffice, Google Sheets

### PDF Export (.pdf)
- High-quality PDF documents
- Professional table formatting
- Includes report title and metadata
- Shows applied filters and generation timestamp
- Alternating row colors for better readability
- Suitable for printing and sharing
- Opens with any PDF reader

## How to Use

### Generating a Report

1. **Navigate to Reports Tab**
   - Click on the "📄 Reports" tab in the main interface

2. **Select Report Type**
   - Choose from the six available report cards

3. **Apply Filters (Optional)**
   - **Date Range**: Enter dates in YYYY-MM-DD format
     - Example: From: 2025-01-01, To: 2025-12-31
     - Leave blank to include all dates
   - **Additional Filters**: Select from dropdown (varies by report type)
     - Students: Filter by year
     - Books: Filter by category
     - Transactions: Filter by status

4. **Export Report**
   - Click **"📊 Export to Excel"** for Excel format
   - Click **"📑 Export to PDF"** for PDF format

5. **Save File**
   - Choose save location
   - Default filename includes report name and timestamp
   - Example: `Students_Report_20260130_143052.xlsx`

6. **Open File (Optional)**
   - After export, you'll be prompted to open the file
   - Click "Yes" to view immediately

## Date Range Filter Tips

- **Empty Date Fields**: Leave date fields empty to include all data
- **From Date Only**: Include all records from that date onwards
- **To Date Only**: Include all records up to that date
- **Both Dates**: Include only records within the specified range
- **Format**: Always use YYYY-MM-DD format (e.g., 2026-01-30)
- **Validation**: Invalid dates will be rejected

## Admin Activity Logging

The system automatically logs the following activities:

### Student Management
- ✅ Student Added: "Added student: [Name] (Enrollment: [No], Year: [Year])"
- ❌ Student Deleted: "Deleted student: [Name] (Enrollment: [No])"
- 🔄 Student Updated: Logged with old and new values

### Book Management
- ✅ Book Added: "Added book: [Title] (ID: [ID], Category: [Category], Copies: [N])"
- ❌ Book Deleted: "Deleted book: [Title] (ID: [ID])"
- 🔄 Book Updated: Logged with changes

### Transactions
- 📤 Book Issued: "Issued book [Book ID] to student [Enrollment]"
- 📥 Book Returned: "Returned book [Book ID] from student [Enrollment] (Fine: ₹X)"

### Promotions
- ⬆️ Student Year Promotion: "Promoted X students. 1st→2nd: Y, 2nd→3rd: Z, 3rd→Pass Out: W"

### Reports
- 📊 Report Export: "Report Export - [Report Name], Format: [Excel/PDF], Filter: [Details]"

## Best Practices

### For Regular Reports
1. **Daily**: Generate overdue books report to follow up with students
2. **Weekly**: Export transactions report for record keeping
3. **Monthly**: Generate comprehensive students and books reports for archives
4. **End of Semester**: Export all reports for academic records

### For Audits
1. Use **Admin Activity Log** to track all system changes
2. Export with date ranges covering the audit period
3. Cross-reference with **Transaction Reports** for verification
4. Keep PDF copies for permanent records

### For Academic Years
1. Use **Promotion History** to track student progression
2. Export before and after each promotion cycle
3. Generate **Students Report** filtered by year for class lists
4. Maintain yearly archives in separate folders

## File Organization Tips

```
Reports/
├── 2025-2026/
│   ├── Students/
│   │   ├── Students_Report_Jan_2026.xlsx
│   │   └── Students_Report_Jan_2026.pdf
│   ├── Books/
│   │   ├── Books_Catalog_Jan_2026.xlsx
│   │   └── Books_Catalog_Jan_2026.pdf
│   ├── Transactions/
│   │   ├── Transactions_Q1_2026.xlsx
│   │   └── Overdue_Report_Jan_2026.xlsx
│   └── Admin/
│       ├── Activity_Log_Jan_2026.pdf
│       └── Promotion_History_2026.pdf
```

## Troubleshooting

### Report Shows "No Data"
- ✅ Check if filters are too restrictive
- ✅ Verify date range includes expected data
- ✅ Ensure there is data in the database for the selected criteria

### Export Failed
- ✅ Check if file location is writable
- ✅ Close any open Excel/PDF files with the same name
- ✅ Ensure sufficient disk space
- ✅ Try a different save location

### Date Filter Not Working
- ✅ Use correct format: YYYY-MM-DD
- ✅ Ensure "From" date is before "To" date
- ✅ Remove placeholder text (YYYY-MM-DD) before entering dates

### PDF Not Opening
- ✅ Ensure a PDF reader is installed
- ✅ Try opening manually from the saved location
- ✅ Check if PDF file was created successfully

## Technical Details

### Database Tables
- **Students**: `students` table
- **Books**: `books` table
- **Transactions**: `transactions` table (joined with students and books)
- **Promotion History**: `promotion_history` table
- **Admin Activity**: `admin_activity` table (auto-created on first use)

### Export Libraries
- **Excel**: pandas + xlsxwriter
- **PDF**: reportlab

### File Naming Convention
```
[Report_Name]_[YYYYMMDD]_[HHMMSS].[extension]
Example: Students_Report_20260130_143052.xlsx
```

## Security & Privacy

- ✅ Reports contain sensitive student information
- ✅ Store exported files securely
- ✅ Admin activity logs all report exports
- ✅ Use appropriate permissions for shared reports
- ✅ Regularly review and archive old reports

## Support

For issues or questions:
- **Developer**: Yash Vijay Date
- **GitHub**: github.com/YashDate31
- **LinkedIn**: linkedin.com/in/yash-date-a361a8329

---

**Last Updated**: January 30, 2026
**Version**: 2.1 (Reports Feature)
