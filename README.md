# IT Helpdesk & Asset Management System

A web-based IT helpdesk application for tracking IT assets, managing support tickets, and monitoring ticket status and history.

## Features

- **Dashboard:** View total IT assets, open tickets, resolved tickets, and recent support tickets.
- **IT Asset Management:** View registered IT assets and their details.
- **Ticket Management:** View support tickets, priorities, assigned assets, and current statuses.
- **Ticket Filtering:** Filter tickets by status and priority.
- **Ticket Status Updates:** Update ticket status and add notes.
- **Ticket History:** Track status changes and associated notes.
- **Database Validation:** Enforce data integrity through database constraints.
- **Error Handling:** Display a custom 404 page for missing tickets.
- **Automated Testing:** Test application routes and database constraints using pytest.

## Technologies Used

- Python 3.12
- Flask 3.1.3
- SQLite
- HTML, CSS, Bootstrap 5
- pytest 9.1.1

## Project Structure

```text
it-helpdesk-asset-management/
├── app.py
├── init_db.py
├── seed_data.py
├── requirements.txt
├── DATABASE_DESIGN.md
├── test_app.py
├── test_db.py
├── db/
│   ├── connection.py
│   ├── asset_repository.py
│   └── ticket_repository.py
├── database/
│   └── helpdesk.db
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── assets.html
│   ├── tickets.html
│   ├── ticket_detail.html
│   └── 404.html
└── static/
    └── css/
        └── style.css
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd it-helpdesk-asset-management
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows CMD:

```cmd
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Initialize the database

Run the database initialization and sample data scripts:

```bash
python init_db.py
python seed_data.py
```

Run these initialization scripts according to their implementation. Reinitializing or reseeding an existing database may affect existing data.

### 5. Start the application

```bash
python -m flask --app app run --debug
```

Open http://127.0.0.1:5000 in your browser.

## Run Tests

Execute the automated test suite:

```bash
python -m pytest -v
```

The current test suite contains 11 tests covering application routes, ticket pages, filtering, and database constraints.

## Sample Data

The sample database includes IT assets such as PCs, printers, and barcode scanners, along with support tickets of different priorities and statuses.

## Project Purpose

This project demonstrates practical skills in Python web development, SQL database design, IT asset tracking, helpdesk ticket management, error handling, and automated testing.
