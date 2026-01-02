# Project Overview

**CURRENT STAGE** Testing Phase

**OBJECTIVE** To bridge the gap between physical libraries and digital learners.
Our goal is to democratize access by building a hybrid ecosystem-parlaying
secure desktop administration with a seamless browser extension-that gives
students instant, 24/7 access to books and study material directly in their
workflow.

### ABSTRACT

Most college libraries are fixed in the past. For students to check a book's
availability or to download notes, they actually have to visit the library.
Resources and learners are quite disconnected from each other. We built the
Integrated Academic Resource Ecosystem-IARE-to solve this "last mile" problem.
Unlike other management systems, IARE is a hybrid solution. It couples a strong
Python Desktop Application for librarians with a lightweight Web Extension for
students. We didn't want to develop yet another awkward portal. Our extension
resides noiselessly in the browser, giving students instant access to the
catalogue and study materials. We even extended the reach of the library beyond
campus; the system includes DELNET integration allowing students to request
books directly from the national library network through the extension, which
the librarian then processes. This transforms the library from a physical room
to a 24/7 digital assistant.

---

# PROBLEM STATEMENT

The conventional university libraries are **functionally isolated**. They depend
on rigid computer software that can be used only by the librarians, making the
students unaware of the same. For searching or accessing study notes, the
students have to actually come to the library, which is not necessary.

Current technology that already exists may be costly or existent only within a
large portal that students do not browse often. Thus, it creates a significant
**resource gap** whereas resources abound within the SFL, students cannot easily
access or research these resources beyond the physical SFL boundaries.

# PROPOSED SOLUTION

We suggest that an "**Integrated Academic Resource Ecosystem**" or "**IARE**" is
developed as a **hybrid solution** that approaches library connectivity with a
new and innovative perspective where "**library administration**" is unbundled
from

**For Administration:** Create a secure Desktop Application in Python for
managing this heavy lifting. The new system is more than an ordinary library
management system that does inventory and fine calculations alone because it has
an intelligent automation system designed for queueing automated due letters to
offenders as well as producing analyses of activities and monthly reports.The
new system is fast and can function even when it is offline.

**For Students:** Rather than designing a portal, we came up with a lightweight
Web Extension. The Web Extension is integrated into the browser so that students
can access and download study materials instantly. We also implemented a
**DELNET Request** service so that students can request national inter-library
materials, and the librarian can receive and process these requests.

This approach solves the problem of **accessibility** because it provides
**resources**, both **local and national**, as well as **automated management
capabilities**, to the users.

---

# Technical Architecture

### METHODOLOGY

_Focus: The engineering approach, architecture, and development life cycle._

The project follows a **Hybrid Modular Architecture** developed using **Agile
Methodology**, thus allowing the iterative development of the desktop and web
modules.

**1. Requirement Analysis:** This gave us the insight about how all the physical
records in the library are not an option that can be availed by the students,
hence, the two modules in which the project will be divided-a powerhouse called
the Admin Panel and the lighter Web Extension that will provide access remotely.

**2. Architectural Design:**

**3. Integration Strategy:** Custom "**Bridge API**" - simulated here by local
file serving, provided a means for the browser extension to read library records
without compromising the main database's security against write access.

### WORKING MECHANISM

The **IARE** is built upon a secure, locally managed Client-Server system
operating in three phases:

---

### KEY FEATURES

- **Real-Time Availability Sync:** Data gets instantly updated as action
  performed on database.
- **Smart SMTP Notification System:** Automatically send Pre-Due Date Reminders
  (2 days before) to students to prevent fines, and Overdue Alerts immediately
  after a deadline is missed.
- **Academic Year-End Promotion :** As academic year promotes it automatically
  promotes students (1st->2nd, 2nd->3rd) and archives graduates ("Pass Out")
- **Automated Overdue Letter Generation:** One-click generation of professional
  Word official warning letters for Overdue cases.
- **Interactive Analytics Dashboard:** Book Circulation Trends, Top Borrowers,
  Most Popular Genres, and Fine Collection Reports & Bulk Data Management: The
  bulk addition of hundreds of students or books via Excel sheets.
- **Hybrid Ecosystem Architecture:** Python Desktop Software for Librarian and
  Web extension for Students.
- **DELNET National Resource Integration:** Students can access DELNET services.
- **Digital Study Material Repository:** Goes beyond physical books by allowing
  admins to upload digital assets (PDF Notes, Past PYQs).

### EXPECTED OUTCOMES

- **Faster Service & Zero Extra Cost:** Reduces book issue and return time to
  under 30 seconds, eliminating student queues & Modernizes the library using
  existing college computers without expensive servers or software fees.
- **24/7 Availability:** Students can check book availability and download notes
  digitally from ecosystem, anytime.
- **Accurate Fines:** Automatically calculates overdue fees, preventing math
  errors.
- **Smart Buying:** Analytics show which books are popular, helping the library
  buy what students actually read.
- **Secure Inventory:** System automatically blocks "Pass Out" students from
  borrowing, preventing book loss.
- **National Reach:** Connects students to the DELNET network to request books
  from outside the college.
- **Data Consistency:** The centralized SQLite database ensures that student
  records and book inventories remain synchronized and duplicate-free across all
  operations.
- **Timely Communication:** The automated scheduler triggers email reminders
  exactly at 9:00 AM (2 days before due dates), ensuring students are notified
  precisely on time.

---

### TECH STACK

**Software**

- **Core & Database:** Python 3.11, SQLite3
- **Desktop Interface & Utilities:** Tkinter, tkcalendar, Pillow (Image
  Processing), PyInstaller (Deployment), qrcode
- **Data Processing & Reports:** Pandas, Matplotlib (Analytics), OpenPyXL,
  xlsxwriter, python-docx (Word Automation)
- **Connectivity & Local Server:** Flask, Waitress, Requests
- **Web Extension (Frontend):** React.js, Vite, Tailwind CSS

**HARDWARE** _None listed_

### BLUEPRINT / DESIGN ASPECT

The first-ever priority was **Simplicity with Reliability**. There were two
important considerations:

### TECHNICAL DOCUMENTS

[View Image]
