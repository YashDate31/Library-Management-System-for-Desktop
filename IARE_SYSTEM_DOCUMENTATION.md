# Project Overview

**CURRENT STAGE** Scaling & Cloud Integration Phase

**OBJECTIVE** To democratize access to academic resources by building a
**Cloud-Native Hybrid Ecosystem** that bridges the gap between physical
libraries and digital learners. We combine standardized desktop administration
with a robust, cloud-synced browser extension to give students instant, 24/7
access to books and study materials directly in their workflow.

### ABSTRACT

Traditional college libraries are often isolated data islands. For students to
check availability or download notes, they must physically visit the library. We
built the **Integrated Academic Resource Ecosystem (IARE)** to solve this "last
mile" problem using modern cloud technologies. unlike legacy systems, IARE is a
**Hybrid Cloud Solution**. It couples a powerful **Python Desktop Application**
for librarians with a lightweight, cloud-connected **Web Extension/Portal** for
students.

By migrating to a **Supabase (PostgreSQL)** backend, the system now ensures
real-time synchronization between the librarian's desktop and the student's
browser, regardless of location. The system also integrates **DELNET** to allow
students to request books from the national library network directly through the
extension. This transforms the library from a room with books into a pervasive
digital assistant.

---

# PROBLEM STATEMENT

1. **Functional Isolation:** Libraries depend on rigid, local-only software.
   Students are unaware of new arrivals or availability unless they are
   physically present.
2. **Resource Gap:** Digital notes, question papers, and references are often
   scattered or inaccessible remotely.
3. **Legacy Tech:** Existing solutions are either expensive,
   enterprise-monolithic portals that students avoid, or archaic offline desktop
   apps.

# PROPOSED SOLUTION

We propose the "**Integrated Academic Resource Ecosystem (IARE)**" – a
**Cloud-Native Hybrid Platform** that unbundles library administration from
access:

**For Administration (The Powerhouse):** A secure, Python-based **Desktop
Application** for heavy lifting. It connects to a cloud-hosted **PostgreSQL
Database (Supabase)**, allowing librarians to manage inventory, queue automated
due letters, and analyze borrowing trends with the speed of a native app but the
connectivity of the cloud.

**For Students (The Access Point):** A lightweight **React Web
Extension/Portal**. It connects directly to the same cloud database, offering
instant search, real-time availability status, and digital downloads. It resides
silently in the browser, meeting students where they already are.

**Key Innovation:** The shift from local SQLite to **Supabase (PostgreSQL)**
implies that the library is "always online." A student checking a book at
midnight sees the exact same status as the librarian at 9:00 AM.

---

# Technical Architecture

### METHODOLOGY

_Focus: Cloud-First Hybrid Engineering_

The project follows a **Hybrid Cloud Architecture**, leveraging the best of
desktop performance and cloud scalability.

**1. Requirement Analysis:** Identified the need for high-performance local
management (scanning, fine calculation) vs. high-availability remote access
(searching, reserving).

**2. Architectural Design:**

- **Database Layer:** **Supabase (PostgreSQL)** acts as the single source of
  truth.
- **Admin Layer:** Python (Tkinter) Desktop App connects via `psycopg2` / API.
- **Student Layer:** React Application (hosted on Vercel/Render) connects via
  Supabase Client.

**3. Integration Strategy:** A "Shared Cloud State" model. The desktop app and
web app read/write to the same Supabase instance, ensuring 0ms latency in data
consistency.

### WORKING MECHANISM

The **IARE** operates as a secure Client-Server system:

1. **Librarian Action:** Scans a book return in the Desktop App.
2. **Cloud Sync:** Desktop App updates the **Supabase PostgreSQL** record
   immediately.
3. **User Update:** Student looking at the Web Portal sees the book status flip
   to "Available" instantly.

---

# KEY FEATURES

- **Cloud-Native Real-Time Sync:** Powered by Supabase, ensuring data
  consistency across all devices instantly.
- **Smart Notification System:** Automated email triggers for "Pre-Due"
  reminders (2 days prior) and "Overdue" alerts using cloud-scheduled jobs or
  background threads.
- **Seamless Graduate Promotion:** Automated logic to promote students (1st->2nd
  Year) and archive alumni ("Pass Out") at the year's end.
- **Automated Document Generation:** One-click generation of professional
  Word/PDF warning letters for overdue cases.
- **Interactive Analytics:** Python-driven dashboards showing Circulation
  Trends, Top Borrowers, and Genre Popularity.
- **DELNET Integration:** A built-in request pipeline for inter-library loans
  from the National Library Network.
- **Digital Repository:** Secure cloud storage for PDF Notes, Previous Year
  Questions (PYQs), and research papers.

### EXPECTED OUTCOMES

- **24/7 Accessibility:** Library is open on every student's laptop, anytime,
  anywhere.
- **Zero Infrastructure Cost:** Using serverless technologies
  (Supabase/Render/Vercel) eliminates the need for expensive on-premise servers.
- **Operational Efficiency:** Reduces book issue/return time to <30 seconds.
- **Data Integrity:** PostgreSQL ensures ACID compliance and robust data
  handling compared to file-based databases.
- **National Connectivity:** Bridges the local college with the national DELNET
  infrastructure.

---

# TECH STACK

### Software & Cloud Infrastructure

- **Core Database:** **Supabase (PostgreSQL)** - The scalable, cloud-native
  backend.
- **Desktop Admin App:**
  - **Language:** Python 3.11+
  - **GUI:** Tkinter (CustomTkinter for modern UI)
  - **Data/Logic:** Pandas, Matplotlib, ReportLab/Python-docx
  - **Connectivity:** `psycopg2-binary`, `requests`, `python-dotenv`
- **Web Portal / Extension:**
  - **Framework:** React.js + Vite
  - **Styling:** Tailwind CSS (Modern, Responsive)
  - **Hosting:** Vercel / Render
- **Backend Services:**
  - **API:** Flask (for specialized endpoints), Gunicorn (Production Server)
  - **Auth:** Supabase Auth / Custom Hash-Based Auth

### HARDWARE

- Standard Windows Desktop/Laptop for Administration.
- Any web-enabled device for Students.

### BLUEPRINT / DESIGN ASPECT

**Priority:** "Simplicity with Reliability." The design decouples the heavy
processing (Admin) from the high-read-traffic (Student), bridged by a robust
Cloud Database. This ensures that heavy student traffic never slows down the
librarian's work.

---

# Impact & Classification

**VALUE ADDITION**

- **Modernization:** Leaps from paper/legacy software to Cloud-Native.
- **Cost-Efficiency:** Utilizes Free-Tier of modern Cloud providers (Supabase,
  Vercel).
- **Scalability:** Can handle thousands of records without local hardware
  upgrades.

**APPLICATION AREAS**

- Government Polytechnics & Engineering Colleges.
- Research Institutions requiring hybrid physical-digital access.

**SOCIAL IMPACT** We remove the physical barrier to knowledge. By placing the
library in the browser, we integrate reading into the student's digital life. It
saves hundreds of librarian hours through automation (fines, reports, letters),
transforming them from "storekeepers" to "knowledge facilitators."

**COMMERCIAL VIABILITY** IARE targets the massive "Digital Transformation"
market in education. Unlike expensive proprietary ERPs, IARE is lightweight,
modular, and can be deployed in minutes using modern CI/CD pipelines. It is a
**Low-Code / No-Code maintenance** solution for the institute.

---

# Institute, District & Team

### INSTITUTE DETAILS

**Government Polytechnic, Awasari (khurd)** _Program:_ Diploma in Computer
Engineering

### LOCATION

**Pune** District

### PROJECT GUIDE / MENTOR

**Ajita Sanjay Patil** _Department:_ Computer Engineering _Email:_
ajitapatilgpa@gmail.com

### TEAM MEMBERS

1. **Yash Vijay Date** - _Lead Developer & Architect_ - yashdate36@gmail.com
2. **Yash Ajay Magar** - _Backend & Database_ - yashajaymagar10@gmail.com
3. **Sharvari Sachin Rokade** - _Frontend & UI/UX_ - sharvari.ssr@gmail.com
4. **Aryan Ramesh Pohakar** - _Documentation & Testing_ -
   pohakar.aryan20@gmail.com

---

# Support Requirements

**Incubation Support Needed:** `YES` **Industry Sponsored:** `NO`

---

# Principal Signed Form

_Declaration: By uploading, I declare this project is original work._
