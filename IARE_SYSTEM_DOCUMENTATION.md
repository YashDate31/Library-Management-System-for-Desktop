# IARE Project Diagrams Walkthrough

This document presents the visual documentation for the **Integrated Academic
Resource Ecosystem (IARE)**. All diagrams use standard industry notations and
have been refined for clarity and proper text fitting.

---

## 1. System Architecture Block Diagram

This high-level diagram illustrates the hybrid nature of the ecosystem, where a
local desktop application serves as the core authority and backend for a
web-based student extension.

```mermaid
graph TD
    classDef storage fill:#f9f,stroke:#333,stroke-width:2px;
    classDef component fill:#dfd,stroke:#333,stroke-width:2px;

    subgraph "Student Layer (Web Extension)"
        FE[/Frontend Browser/]:::component
    end

    subgraph "Logic & Service Layer"
        Waitress[Waitress/Flask<br/>Local Web Server]:::component
        AdminUI[Tkinter Admin<br/>Desktop Application]:::component
    end

    subgraph "External Integration"
        SMTP[GMail SMTP Server]:::component
    end

    subgraph "Data Layer"
        PDB[(portal.db)]:::storage
        LDB[(library.db)]:::storage
    end

    FE -- "HTTPS/API<br/>Requests" --> Waitress
    Waitress -- "CRUD" --> PDB
    AdminUI -- "Direct Query" --> LDB
    AdminUI -- "Manage" --> PDB
    AdminUI -- "Alerts" --> SMTP
```

### In-Depth Explanation:

The architecture is a **Hybrid Decentralized Model**.

- **The Student Layer**: Operates as a thin client (Web Extension) that
  communicates via an API.
- **The Logic Layer**: Is dual-purpose. The **Waitress/Flask** server handles
  non-blocking web requests (booking requests, profile views), while the
  **Tkinter Admin App** provides a heavy-duty UI for the librarian to perform
  physical transactions.
- **The Data Layer**: Uses two separate SQLite databases to decouple core
  library inventory (`library.db`) from volatile portal requests (`portal.db`),
  ensuring system stability even if the web service is under load.

---

## 2. Feature 1: Book Reservation / Request Workflow

This flow depicts the asynchronous "Request -> Approval" queue, where a student
expresses interest, but no inventory is moved until administrative intervention.

```mermaid
flowchart TD
    Start([Start]) --> Input[/Student Enters<br/>Request Details/]
    Input --> API[POST /api/request]
    API --> Validate{Valid<br/>Session?}
    
    Validate -- No --x Stop([End: Invalid])
    Validate -- Yes --> DBInsert[(Insert to portal.db<br/>status: 'pending')]
    
    DBInsert --> Refresh[/Librarian Refreshes<br/>Dashboard/]
    Refresh --> ViewCard[View Pending<br/>Request Card]
    
    ViewCard --> Decision{Librarian<br/>Approves?}
    
    Decision -- No --x EndReject([Request Ignored])
    Decision -- Yes --> UpdateDB[Update Status:<br/>'approved']
    
    UpdateDB --> SMTP[Trigger SMTP Email<br/>'Ready for Pickup']
    SMTP --> EndSuccess([End: Ready for Pickup])
```

### In-Depth Explanation:

1. **Initiation**: The student starts by submitting a request through the
   extension. This is a non-committal data entry.
2. **Server Validation**: The Flask API validates the session before writing to
   the `requests` table in `portal.db`. The status is explicitly set to
   `pending`.
3. **Human-in-the-Loop**: Unlike automated e-commerce, this system requires a
   Librarian's manual review. This prevents inventory locking by inactive
   students.
4. **Completion**: Once approved, the system transitions from a database update
   to an external side-effect (sending an email via SMTP), notifying the student
   that the physical book is now being held for them.

---

## 3. Feature 2: Transaction Cycle (Issue & Return)

The core physical operations of the library. These flows follow strict
validation rules to maintain inventory integrity.

#### Book Issue Process

```mermaid
flowchart TD
    Start([Start Issue]) --> In[/Input: Enrollment No<br/>& Book ID/]
    In --> Val1{Student<br/>Pass Out?}
    
    Val1 -- Yes --x Block1([Block: Invalid Status])
    Val1 -- No --> Val2{Available<br/>Copies > 0?}
    
    Val2 -- No --x Block2([Block: Out of Stock])
    Val2 -- Yes --> Val3{Student at<br/>Max Limit?}
    
    Val3 -- Yes --x Block3([Block: Limit Exceeded])
    Val3 -- No --> Action[Insert Record to<br/>borrow_records]
    
    Action --> DB[Update library.db:<br/>Decrement Available]
    DB --> Success([End: Book Issued])
```

#### Book Return Process

```mermaid
flowchart TD
    Start([Start Return]) --> In[/Input: Book ID/]
    In --> Logic[Calculate:<br/>Days_Late = Now - Due_Date]
    
    Logic --> FineCheck{Days_Late > 0?}
    
    FineCheck -- Yes --> SetFine[Fine = Days * 5 INR]
    FineCheck -- No --> NoFine[Fine = 0]
    
    SetFine --> Update
    NoFine --> Update
    
    Update[Update borrow_records:<br/>Set Return Date & status='returned'] --> Incr[Update library.db:<br/>Increment Available]
    Incr --> End([End: Book Returned])
```

### In-Depth Explanation:

- **Issue Workflow**: This is a **Guard-Pattern** flow. The system checks three
  critical conditions (Student Status, Content Availability, and Borrowing
  Limits) before allowing a database write. This ensures the library never
  over-promises or issues books to inactive students.
- **Return Workflow**: This is a **Calculation-First** flow. The priority is
  determining financial liability (Fine) before resetting the inventory status.
  The incrementing of `available_copies` only happens after the transaction
  record is closed.

---

## 4. Feature 4: Analytics/Graph Generation

Visual representation of library health through dynamic data processing.

```mermaid
flowchart LR
    Data[/Query library.db<br/>borrow_records/] --> Map[Python/Sqlite3<br/>Processing Logic]
    
    subgraph "Metrics Extracted"
        M1[Active Loans Count]
        M2[Overdue Count]
        M3[Popularity Rankings]
    end
    
    Data --> Map
    Map --> M1 & M2 & M3
    
    M1 & M2 & M3 --> Render[Matplotlib<br/>Rendering Engine]
    Render --> Canvas[Tkinter GUI<br/>Canvas Widget]
    Canvas --> Reveal([Display Pie/Bar Charts])
```

### In-Depth Explanation:

- **Data Acquisition**: The system performs aggregate SQL queries (e.g.,
  `COUNT`, `GROUP BY`) on the `borrow_records` table.
- **Processing**: Python logic cleans this data, handling dates and status
  strings to ensure the counts are accurate for the "Analysis" tab.
- **Integration**: IARE uses **Matplotlib** for high-fidelity scientific
  plotting. The resulting chart is not a static image but a live-rendered
  component embedded directly into the Tkinter application's layout.

---

## 5. Feature 5: DELNET / External Resource Request

Managing resources that exist outside the local library's inventory.

```mermaid
flowchart TD
    SReq([Student Submits<br/>External Request]) --> Payload[/JSON Payload:<br/>Source: 'DELNET'/]
    Payload --> Storage[(portal.db)]
    
    Storage --> Dashboard[Librarian Dashboard<br/>'External' Tab]
    Dashboard --> Offline[Process Request<br/>via External DELNET Portal]
    
    Offline --> Arrived{Resource<br/>Received?}
    
    Arrived -- Yes --> Final[Librarian Marks<br/>'Approved']
    Final --> Notify[Automated Email Notification]
    Notify --> End([Resource Ready])
```

### In-Depth Explanation:

This workflow is a **Proxy-Process**.

- **The Digital Shell**: The student uses the IARE extension to create a digital
  trace of their request.
- **The Physical Bridge**: The Librarian acts as the coordinator with the
  external DELNET network.
- **Closing the Loop**: Once the resource physically arrives, the Librarian
  updates the status in IARE, which triggers the digital notification system
  (SMTP) to alert the student.

---

## 6. Feature 6: Automated Email Logic

The background "Watchdog" process that ensures students are reminded of their
deadlines.

```mermaid
flowchart TD
    Start([App Startup]) --> Thread[Spawn Background Thread]
    Thread --> Sleep[Calculate Sleep Time<br/>Until 09:00 AM]
    
    Sleep --> Trigger([Daily Execution])
    Trigger --> Query[/Query records due in<br/>'Today + 2 Days'/]
    
    Query --> SMTP[Init SMTP Session<br/>Port 587]
    SMTP --> Loop{Iterate<br/>Recipients}
    
    Loop -- Next --> Send[Send Pre-Due Email]
    Send --> History[Log to email_history.json]
    History --> Loop
    
    Loop -- Done --> Sleep
```

### In-Depth Explanation:

- **Persistence**: Unlike standard UI actions, this is a **Daemon Process** that
  runs as long as the Admin App is open.
- **Timing Constraint**: It uses a smart sleep logic to avoid spamming; it only
  activates once a day at 09:00 AM.
- **The 2-Day Rule**: The logic specifically targets users whose deadline is
  exactly 48 hours away, providing a "Pre-Due" cushion.
- **Fault Tolerance**: Every action is logged to `email_history.json`, allowing
  the Librarian to audit if reminders are actually being delivered.
