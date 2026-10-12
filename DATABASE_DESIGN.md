# Database Design

## IT Helpdesk & Asset Management System

### 1. assets

- id: Primary Key
- asset_tag: Unique asset identifier
- asset_type: PC, Printer, Barcode Scanner
- serial_number: Device serial number
- assigned_to: Assigned employee
- location: Department or factory location
- status: Active, Maintenance, Retired

### 2. tickets

- id: Primary Key
- title: Issue title
- description: Issue details
- priority: Low, Medium, High, Critical
- status: Open, In Progress, Resolved, Closed
- asset_id: Foreign Key referencing assets.id
- created_at: Ticket creation time
- resolved_at: Resolution time

### 3. ticket_history

- id: Primary Key
- ticket_id: Foreign Key referencing tickets.id
- old_status: Previous ticket status
- new_status: Updated ticket status
- note: Technician's work note
- changed_at: Change timestamp

## Relationships

- One asset can have many tickets.
- One ticket can have many history records.
- Tickets may exist without an associated asset.
