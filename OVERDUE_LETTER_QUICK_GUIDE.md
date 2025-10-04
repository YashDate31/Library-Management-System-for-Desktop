# 📬 Overdue Letter Feature - Quick Reference

## How to Send Overdue Letter

### ⚡ Quick Steps:
1. **Open** Records Tab
2. **Find** overdue record (yellow background)
3. **Double-click** on the record
4. **Confirm** in dialog box
5. **Save** Word document
6. **Done!** ✅

---

## 🎯 What You Need

- An **overdue** borrowed book record
- The book must have:
  - ✅ Status = "Borrowed" (not returned yet)
  - ✅ Due date passed
  - ✅ Fine > 0

---

## 📋 Letter Contains

- Library header
- Current date
- Student details (Name, Enrollment No)
- Book details (ID, Title, Issue Date, Due Date)
- Days overdue
- Fine amount
- Request message
- Librarian signature

---

## 💡 Tips

### Find Overdue Books Fast:
- Use **Type Filter** → Select "Overdue"
- Use **Quick Filters** → "Last 7/15/30 Days"
- Look for **yellow background** rows

### Save Multiple Letters:
- Create folder: `Overdue_Letters/October_2025/`
- Generate all letters at once
- Print together

### Can't Double-Click?
- Make sure record shows fine: `20 (Late)`
- Yellow background indicates overdue
- White background = not overdue (can't generate letter)

---

## ⚠️ Error Messages

| Message | Meaning | Solution |
|---------|---------|----------|
| "Not Overdue" | Record is returned or not late | Only use for overdue records |
| "python-docx not installed" | Missing library | Run: `pip install python-docx` |

---

## 📁 File Format

- **Extension:** .docx (Microsoft Word)
- **Filename:** `Overdue_Letter_[EnrollmentNo]_[DateTime].docx`
- **Example:** `Overdue_Letter_CS2024001_20251003_143025.docx`

---

## 🎨 Visual Guide

```
Records Tab
┌─────────────────────────────────────────────────────────┐
│ 📊 Records                                              │
├─────────────────────────────────────────────────────────┤
│ Search: [        ]  Type: [Overdue ▼]                  │
│ ┌─────────────────────────────────────────────┐         │
│ │ Enrollment │ Name   │ Book    │ Fine       │ ← Yellow│
│ │ CS2024001  │ Rahul  │ Algo    │ 20 (Late)  │   BG    │
│ │ CS2024005  │ Priya  │ Python  │ 15 (Late)  │ ← Double│
│ │ CS2024012  │ Amit   │ Java    │ 10 (Late)  │   Click │
│ └─────────────────────────────────────────────┘   Here! │
└─────────────────────────────────────────────────────────┘
                    ↓ Double-Click
┌─────────────────────────────────────────────────────────┐
│ Send Overdue Letter                              [?]    │
├─────────────────────────────────────────────────────────┤
│ Send overdue letter to:                                 │
│                                                          │
│ Student: Rahul Sharma                                   │
│ Enrollment: CS2024001                                   │
│ Book: Introduction to Algorithms                        │
│ Fine: 20 (Late)                                         │
│                                                          │
│ Generate Word document?                                 │
│                                                          │
│              [Yes]        [No]                          │
└─────────────────────────────────────────────────────────┘
                    ↓ Click Yes
┌─────────────────────────────────────────────────────────┐
│ Save As                                          [?]    │
├─────────────────────────────────────────────────────────┤
│ Save in: Documents ▼                                    │
│                                                          │
│ File name: Overdue_Letter_CS2024001_20251003.docx      │
│ Save as type: Word Document (*.docx) ▼                 │
│                                                          │
│              [Save]       [Cancel]                      │
└─────────────────────────────────────────────────────────┘
                    ↓ Click Save
┌─────────────────────────────────────────────────────────┐
│ Success                                          [✓]    │
├─────────────────────────────────────────────────────────┤
│ Overdue letter generated successfully!                  │
│                                                          │
│ Saved to:                                               │
│ C:\Users\...\Documents\Overdue_Letter_CS2024001.docx   │
│                                                          │
│                     [OK]                                │
└─────────────────────────────────────────────────────────┘
                    ↓ Click OK
┌─────────────────────────────────────────────────────────┐
│ Open Document                                    [?]    │
├─────────────────────────────────────────────────────────┤
│ Do you want to open the document now?                   │
│                                                          │
│              [Yes]        [No]                          │
└─────────────────────────────────────────────────────────┘
                    ↓ Click Yes
        (Microsoft Word opens with letter)
```

---

## 📄 Letter Preview

```
        LIBRARY OF COMPUTER DEPARTMENT

                            Date: October 03, 2025

              Subject: Overdue Book Notice

To,
Rahul Sharma
Enrollment No: CS2024001

Dear Rahul Sharma,

This is to inform you that the following book...

Book Details:
┌────────────┬──────────────────────────┐
│ Book ID:   │ 15                       │
│ Book Title:│ Introduction to Algo...  │
│ Issue Date:│ 2025-09-15              │
│ Due Date:  │ 2025-09-29              │
│ Days OD:   │ 4                        │
└────────────┴──────────────────────────┘

Current fine: ₹20

Please return immediately...

Yours sincerely,
Librarian
Library of Computer Department
```

---

## ✅ Checklist

Before Generating Letter:
- [ ] Record is overdue (yellow background)
- [ ] Status shows "Borrowed"
- [ ] Fine shows "(Late)"

After Generating:
- [ ] Letter saved successfully
- [ ] Document opens in Word
- [ ] All details are correct
- [ ] Print or email to student
- [ ] Keep copy for records

---

## 🔄 Monthly Workflow

**Week 1:** Monitor new overdue
**Week 2:** Generate first reminders
**Week 3:** Generate second reminders
**Week 4:** Generate final notices + escalate

---

## 📞 Quick Help

**Issue:** Can't generate letter  
**Fix:** Check if record is truly overdue (yellow + Late)

**Issue:** Document won't open  
**Fix:** Navigate to saved location, open manually

**Issue:** Wrong student details  
**Fix:** Update student info in Students tab first

---

## 🎓 Remember

- **One Double-Click** = One Letter
- **Yellow Background** = Can Generate Letter
- **White Background** = Cannot Generate Letter
- **Save First** = Then Print/Email

---

**Version:** 4.2  
**Date:** October 3, 2025  
**Status:** ✅ Active

---

Need detailed help? See **OVERDUE_LETTER_FEATURE.md**
