# New Requirements (Teacher Requests)

1. Enforce exactly 7-day loan period (Due Date = Borrow Date + 7 days).
2. When a book is returned late (return_date > due_date) show a punishment/late popup message.

Implementation summary:
- Added `LOAN_PERIOD_DAYS = 7` constant (main.py) near existing constants.
- Updated `database.borrow_book` to validate the due date difference.
- Updated UI defaults (borrow form) to prefill due date with borrow date + 7.
- Modified `return_book` method (main.py) to detect overdue return and show special warning dialog with fine & overdue days.
