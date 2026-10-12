import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "helpdesk.db"


def seed_data():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        # Sample IT assets
        conn.executemany(
            """
            INSERT INTO assets (
                asset_tag, asset_type, serial_number,
                assigned_to, location, status
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(asset_tag) DO NOTHING
            """,
            [
                ("PC-001", "PC", "SN-PC-001", "Nguyen Van A", "IT Office", "Active"),
                (
                    "PRN-001",
                    "Printer",
                    "SN-PRN-001",
                    "Tran Van B",
                    "Production Line 1",
                    "Active",
                ),
                (
                    "BCS-001",
                    "Barcode Scanner",
                    "SN-BCS-001",
                    "Le Van C",
                    "Warehouse",
                    "Active",
                ),
            ],
        )

        # Retrieve asset IDs by asset tag
        assets = dict(
            conn.execute(
                "SELECT asset_tag, id FROM assets WHERE asset_tag IN (?, ?, ?)",
                ("PC-001", "PRN-001", "BCS-001"),
            ).fetchall()
        )

        # Sample helpdesk tickets
        conn.executemany(
            """
            INSERT INTO tickets (
                title, description, priority, status, asset_id
            )
            SELECT ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM tickets WHERE title = ?
            )
            """,
            [
                (
                    "PC cannot connect to network",
                    "The workstation cannot access the company network.",
                    "High",
                    "Open",
                    assets["PC-001"],
                    "PC cannot connect to network",
                ),
                (
                    "Printer cannot print labels",
                    "The production printer does not print barcode labels.",
                    "Critical",
                    "In Progress",
                    assets["PRN-001"],
                    "Printer cannot print labels",
                ),
                (
                    "Barcode scanner not responding",
                    "The warehouse scanner does not read barcodes.",
                    "Medium",
                    "Resolved",
                    assets["BCS-001"],
                    "Barcode scanner not responding",
                ),
            ],
        )

        # Add history records for tickets that do not have history yet
        conn.execute(
            """
            INSERT INTO ticket_history (
                ticket_id, old_status, new_status, note
            )
            SELECT t.id, NULL, t.status, 'Initial sample ticket status'
            FROM tickets AS t
            WHERE t.title IN (?, ?, ?)
              AND NOT EXISTS (
                  SELECT 1
                  FROM ticket_history AS h
                  WHERE h.ticket_id = t.id
              )
            """,
            (
                "PC cannot connect to network",
                "Printer cannot print labels",
                "Barcode scanner not responding",
            ),
        )

    print("Sample data inserted successfully!")


if __name__ == "__main__":
    seed_data()
