# Export Records Bug Fix

Issue: Exporting records failed due to mismatch between data tuple length (9) and column headers provided (8).

Data returned from `get_all_records()`:
(enrollment_no, student_name, book_id, book_title, borrow_date, due_date, return_date, status, fine)

Original export columns:
['Record ID','Student Name','Book Title','Borrow Date','Due Date','Return Date','Status','Days Overdue'] (length 8)

Resolution: Updated columns to align with data and reflect UI table:
['Enrollment No','Student Name','Book ID','Book Title','Borrow Date','Due Date','Return Date','Status','Fine']

This mirrors `record_columns` used in the Records tab.
