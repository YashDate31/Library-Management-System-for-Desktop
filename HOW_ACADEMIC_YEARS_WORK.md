# How Academic Years Are Generated

## 🎓 Academic Year System Explained

---

## 📚 What is Academic Year?

The academic year tracks when students borrow books and get promoted. It helps you:
- Filter records by year (e.g., see all 2024-2025 activities)
- Track promotion history
- Organize library activities by academic session

---

## 🔄 How New Academic Years Are Created

### ✨ Automatic Creation

**New academic years are created AUTOMATICALLY when you promote students!**

### When You Promote Students:

1. **Open Promote Students Dialog**
   - Go to **Manage** → **Promote Students to Next Year**

2. **Academic Year Field Shows Suggestion**
   - The field auto-suggests next year
   - Example: If current is 2025-2026, it suggests 2026-2027

3. **You Can Change It**
   - Accept the suggestion, OR
   - Type your own year (e.g., 2027-2028)

4. **When You Click "Promote All"**
   - System creates the new academic year automatically
   - Sets it as the ACTIVE year
   - Deactivates all previous years
   - All students get promoted
   - All future book issues are tagged with this year

---

## 📋 Step-by-Step Example

### Scenario: Promoting Students in October 2025

```
Current Active Year: 2025-2026

Step 1: Click "Manage" → "Promote Students to Next Year"
        
Step 2: Promotion Dialog Opens
        ┌─────────────────────────────────────┐
        │ Letter Number: [PROMO-2026-1]       │
        │ Academic Year: [2026-2027]           │ ← Auto-suggested!
        │                                     │
        │ [Promote All] [Undo Last] [History] │
        └─────────────────────────────────────┘

Step 3: Click "Promote All"
        
Step 4: System Automatically:
        ✅ Creates academic year "2026-2027"
        ✅ Makes "2026-2027" the ACTIVE year
        ✅ Deactivates "2025-2026"
        ✅ Promotes all students (1st→2nd, 2nd→3rd, 3rd→Pass Out)
        ✅ Records promotion with letter number
        
Step 5: Future Book Issues
        All books borrowed after this will be tagged as "2026-2027"
```

---

## 🎯 Academic Year Auto-Suggestion Logic

The system is smart! It suggests the next year based on:

### Current Date Logic:
```
If Month >= July (New academic year starts):
    Current Year: 2025-2026
    Suggested: 2026-2027

If Month < July (Still in current academic year):
    Current Year: 2024-2025
    Suggested: 2025-2026
```

### Example Calendar:

```
January 2025:   Suggests 2025-2026 (we're in 2024-2025)
July 2025:      Suggests 2025-2026 (new year starts)
October 2025:   Suggests 2026-2027 (we're in 2025-2026)
January 2026:   Suggests 2026-2027 (we're in 2025-2026)
July 2026:      Suggests 2026-2027 (new year starts)
```

---

## 💡 How to Use Different Academic Years

### Option 1: Accept Auto-Suggestion (Recommended)
```
Dialog shows: 2026-2027
Action: Just click "Promote All"
Result: Creates 2026-2027 automatically
```

### Option 2: Custom Academic Year
```
Dialog shows: 2026-2027
Action: Delete and type "2027-2028"
Click: "Promote All"
Result: Creates 2027-2028 instead
```

### Option 3: Use Existing Year
```
Dialog shows: 2026-2027
Action: Change to existing year like "2025-2026"
Click: "Promote All"
Result: Activates 2025-2026 (doesn't create new)
```

---

## 🗄️ Database Structure

### Academic Years Table:
```sql
CREATE TABLE academic_years (
    id INTEGER PRIMARY KEY,
    year_name TEXT UNIQUE,           -- e.g., "2025-2026"
    is_active INTEGER DEFAULT 0,     -- 1 = active, 0 = inactive
    created_at TIMESTAMP
);
```

### Current Database:
```
┌────┬─────────────┬───────────┬─────────────────────┐
│ ID │ Year Name   │ Is Active │ Created At          │
├────┼─────────────┼───────────┼─────────────────────┤
│ 1  │ 2025-2026   │ 1         │ 2025-10-03 12:30:00 │ ← ACTIVE
└────┴─────────────┴───────────┴─────────────────────┘
```

### After Promotion:
```
┌────┬─────────────┬───────────┬─────────────────────┐
│ ID │ Year Name   │ Is Active │ Created At          │
├────┼─────────────┼───────────┼─────────────────────┤
│ 1  │ 2025-2026   │ 0         │ 2025-10-03 12:30:00 │ ← Deactivated
│ 2  │ 2026-2027   │ 1         │ 2025-10-03 14:45:00 │ ← NEW & ACTIVE
└────┴─────────────┴───────────┴─────────────────────┘
```

---

## 🔍 Where Academic Year is Used

### 1. Book Borrowing
When a student borrows a book:
```python
Issue Book → Saves record with active academic year
Result: Book record tagged as "2025-2026"
```

### 2. Records Filter
In Records tab:
```
Academic Year dropdown shows:
- All Academic Years (default)
- 2025-2026
- 2026-2027
- 2027-2028 (all available years)

Select one to filter records from that year only
```

### 3. Promotion History
Each promotion is linked to an academic year:
```
Letter Number: PROMO-2026-1
Academic Year: 2026-2027
Date: 2025-10-03
Students Promoted: 45
```

---

## 📊 Academic Year Lifecycle

```
┌─────────────────────────────────────────────────────┐
│ Timeline: Academic Year Lifecycle                    │
│ Academic Year: July to June                          │
└─────────────────────────────────────────────────────┘

July 2025:
  └─ Academic Year 2025-2026 starts
     ├─ Books borrowed → Tagged as "2025-2026"
     ├─ Records show "2025-2026"
     └─ This is the ACTIVE year

June 2026:
  └─ Time to promote students!
     ├─ Click "Promote Students"
     ├─ System suggests "2026-2027"
     └─ Click "Promote All"

Promotion Happens:
  ├─ Creates new year "2026-2027"
  ├─ Deactivates "2025-2026"
  ├─ Promotes all students
  └─ 2026-2027 is now ACTIVE

July 2026 onwards:
  └─ New academic year 2026-2027 active
     ├─ Books borrowed → Tagged as "2026-2027"
     ├─ Records show "2026-2027"
     └─ Old records still show "2025-2026"

June 2027:
  └─ Repeat the cycle!
     └─ Promote to 2027-2028
```

---

## ⚙️ Technical Details

### Function: `create_academic_year(year_name)`

**What it does:**
1. Deactivates ALL existing academic years
2. Checks if year already exists:
   - If YES: Just activates it
   - If NO: Creates new entry and activates it
3. Returns success message

**Code Flow:**
```python
def create_academic_year(self, year_name):
    # Step 1: Deactivate all years
    UPDATE academic_years SET is_active = 0
    
    # Step 2: Try to insert new year
    try:
        INSERT INTO academic_years (year_name, is_active) 
        VALUES ('2026-2027', 1)
    except IntegrityError:  # Year already exists
        # Just activate the existing year
        UPDATE academic_years 
        SET is_active = 1 
        WHERE year_name = '2026-2027'
```

---

## 🎓 Manual Academic Year Creation

If you need to create an academic year WITHOUT promoting:

### Option 1: Using Script
```python
# Run from LibraryApp folder
python add_academic_year.py
```

### Option 2: Direct Database
```sql
-- Insert new year
INSERT INTO academic_years (year_name, is_active) 
VALUES ('2027-2028', 0);

-- To activate it:
UPDATE academic_years SET is_active = 0;  -- Deactivate all
UPDATE academic_years 
SET is_active = 1 
WHERE year_name = '2027-2028';  -- Activate specific
```

---

## 🚨 Important Notes

### ✅ DO:
- Let the system auto-suggest academic year
- Promote students once per year
- Use format "YYYY-YYYY" (e.g., 2025-2026)
- Check which year is active before issuing books

### ❌ DON'T:
- Create academic years manually (let promotion do it)
- Use wrong format (e.g., "2025" or "25-26")
- Promote students multiple times in same year
- Delete academic years (can cause data loss)

---

## 💡 Pro Tips

### Tip 1: Check Active Year
Before issuing books:
```
Records Tab → Academic Year dropdown
The one marked as "Active" is current
```

### Tip 2: View Historical Data
```
Records Tab → Select Academic Year "2024-2025"
Shows all books borrowed in that year
```

### Tip 3: Promotion Best Practice
```
Promote students at end of academic year (June)
This keeps the data organized by year
Academic Year runs from July to June
```

### Tip 4: Academic Year Naming
```
Use: 2025-2026, 2026-2027, 2027-2028
Avoid: 2025, 25-26, 2025-26
Standard format makes filtering easier
```

### Tip 5: Send Overdue Letters Quickly
```
Records Tab → Find overdue record (yellow highlighted)
Double-click on the record → Generates Word letter instantly
Perfect for sending personal overdue notices!
```

---

## 🎯 Summary

### How New Years Are Created:
**AUTOMATIC during student promotion!**

### Steps:
1. Click "Promote Students"
2. System suggests next year (e.g., 2026-2027)
3. Accept or change the year
4. Click "Promote All"
5. New year created automatically!

### What Gets Created:
- New academic year entry in database
- Year is set as ACTIVE
- All previous years become INACTIVE
- Future book issues tagged with new year

### Benefits:
- ✅ No manual year creation needed
- ✅ Automatic year tracking
- ✅ Easy filtering by year
- ✅ Clear promotion history
- ✅ Organized library records

---

## 🎉 Example Workflow

**Today: October 3, 2025**

```
Step 1: Current active year is 2025-2026

Step 2: Students need promotion for next session

Step 3: Open "Promote Students to Next Year"

Step 4: System shows:
        Letter Number: [PROMO-2026-1]
        Academic Year: [2026-2027] ← Auto-suggested!

Step 5: Click "Promote All"

Step 6: Magic happens! ✨
        - Academic year 2026-2027 created
        - Set as active year
        - All students promoted
        - Promotion recorded in history

Step 7: From now on:
        - Books borrowed = Tagged as "2026-2027"
        - Records filter shows "2026-2027"
        - Old records still accessible by selecting "2025-2026"
```

---

**That's it! The system handles everything automatically!** 🎉

---

**Version**: 4.2  
**Last Updated**: October 3, 2025  
**Feature**: Academic Year Auto-Generation
