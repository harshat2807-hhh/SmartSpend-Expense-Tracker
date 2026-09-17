# SmartSpend – Personal Expense Tracker

## 🚀 Live Demo

[Open SmartSpend Live Website](https://smartspend-expense-tracker-xrbp.onrender.com)




# SmartSpend – Personal Expense Tracker

SmartSpend is a modern, responsive full-stack personal finance web application built with **Python Flask**, **SQLite**, and vanilla **HTML5/CSS3/JavaScript (Fetch API)**. It enables users to track daily expenses, categorize transactions, view live financial analytics, and maintain complete control over their personal budget.

---

## Table of Contents
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Architecture & Folder Structure](#architecture--folder-structure)
- [Database Schema & Design](#database-schema--design)
- [API Endpoints & CRUD Explanation](#api-endpoints--crud-explanation)
- [Installation & Setup](#installation--setup)
- [How to Run](#how-to-run)
- [Testing & Verification](#testing--verification)
- [Future Enhancements](#future-enhancements)

---

## Problem Statement
Individuals frequently struggle to monitor their daily expenses, leading to poor budgeting decisions, unexpected monthly overspending, and lack of clarity on financial habits. Existing financial tools can be bloated or require intrusive setup. **SmartSpend** offers an intuitive, lightweight, real-time solution to record, categorize, search, and analyze expenses effortlessly.

---

## Objectives
1. Provide a zero-overhead personal expense tracker web application.
2. Implement robust backend CRUD APIs powered by Python Flask and SQLite.
3. Deliver a dynamic user interface using native JavaScript Fetch API without page refreshes.
4. Enforce strict input validation on both client and server sides.
5. Offer instant search, category filtering, and live dashboard metrics calculation.

---

## Key Features
- **Live Financial Dashboard**: Automatically calculates and updates **Total Spent**, **Total Expense Count**, and **Average Expense**.
- **Complete CRUD Functionality**: Create, read, edit/update, and delete expenses.
- **Categorization & Payment Methods**: Categorize transactions under Food, Travel, Education, Shopping, Bills, Entertainment, Health, or Other, with supported payment modes (Cash, UPI, Card, Net Banking).
- **Dynamic Search & Filtering**: Real-time title search and category-wise filtering without page reloads.
- **Dual-Layer Validation**: Frontend and backend validation preventing empty values or invalid/non-positive numbers.
- **Modern Dark UI**: Designed with glassmorphic cards, smooth hover effects, colorful category badges, toast notifications, and custom confirmation modals.

---

## Tech Stack
- **Frontend**: HTML5, CSS3 (Vanilla CSS with Custom Properties), JavaScript (ES6+, Fetch API)
- **Backend**: Python 3, Flask Web Framework
- **Database**: SQLite3
- **Iconography & Fonts**: FontAwesome 6, Google Fonts (Outfit)

---

## Architecture & Folder Structure

```
Expense Tracker/
├── app.py              # Flask server, routes, SQLite DB helper & API logic
├── requirements.txt    # Python package dependencies
├── README.md           # Comprehensive project documentation
├── templates/
│   └── index.html      # Main Single-Page HTML interface
└── static/
    ├── style.css       # Custom dark/glassmorphic responsive styling
    └── script.js        # Vanilla JS Fetch API client & UI event handling
```

---

## Database Schema & Design

The application automatically creates the `expenses.db` database and `expenses` table upon initialization.

```sql
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    notes TEXT
);
```

---

## API Endpoints & CRUD Explanation

| Method | Endpoint | Description | Request Body (JSON) | Response Status |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/api/expenses` | Retrieve all expenses | None | `200 OK` |
| **GET** | `/api/expenses/<id>` | Retrieve single expense by ID | None | `200 OK` / `404 Not Found` |
| **POST** | `/api/expenses` | Create a new expense | `{ title, amount, category, date, payment_method, notes }` | `201 Created` / `400 Bad Request` |
| **PUT** | `/api/expenses/<id>` | Update an existing expense | `{ title, amount, category, date, payment_method, notes }` | `200 OK` / `400 Bad Request` / `404 Not Found` |
| **DELETE** | `/api/expenses/<id>` | Delete expense by ID | None | `200 OK` / `404 Not Found` |

### CRUD Operations Breakdown:
1. **CREATE (`POST /api/expenses`)**: Validates input data, formats `amount` as float, executes parameterized `INSERT INTO expenses`, and returns the newly created record with HTTP 201.
2. **READ ALL (`GET /api/expenses`)**: Queries all records from SQLite sorted by date (descending), returns a JSON array with HTTP 200.
3. **READ ONE (`GET /api/expenses/<id>`)**: Fetches expense matching ID or returns HTTP 404 error response if not found.
4. **UPDATE (`PUT /api/expenses/<id>`)**: Verifies ID existence, validates new input parameters, executes parameterized `UPDATE expenses`, and returns the updated object with HTTP 200.
5. **DELETE (`DELETE /api/expenses/<id>`)**: Validates ID, executes `DELETE FROM expenses WHERE id = ?`, and returns confirmation JSON with HTTP 200.

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher installed on your system.

### Steps
1. Navigate to the project directory:
   ```bash
   cd "c:\Expense Tracker"
   ```

2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   ```

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Run

1. Start the Flask application server:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## Testing & Verification

1. **Test Expense Creation**:
   - Fill out Title (e.g. "Textbooks"), Amount (e.g. `450`), Category ("Education"), Date, Payment Method ("UPI"), Notes ("Semester 1").
   - Click **Add Expense**. Verify the toast notification appears and the new row is added to the table.
2. **Test Validation**:
   - Try submitting an empty title or negative amount (`-50`). Confirm inline red error messages and toast warnings.
3. **Test Dashboard Update**:
   - Observe Total Spent, Total Expenses, and Average Expense update instantly after adding/editing/deleting records.
4. **Test Live Search & Filter**:
   - Type in the search box to filter by title.
   - Select a specific Category from the dropdown (e.g., "Food"). Confirm matching results are filtered without reloading the page.
5. **Test Editing**:
   - Click the pencil icon on an expense. Verify the form populates, button changes to "Update Expense", edit the amount, and submit.
6. **Test Deletion**:
   - Click the trash icon. Confirm the deletion modal opens. Click **Delete** and ensure the record is removed from the SQLite database.

---

## Future Enhancements
- Monthly budget limits with alert threshold notifications.
- Visual charts (Pie chart by Category & Monthly trend chart using Chart.js).
- Export expense history to CSV / PDF format.
- Multi-currency conversion support.
