import sqlite3
from pathlib import Path

import pytest

DB_PATH = Path(__file__).resolve().parent / "database" / "helpdesk.db"


@pytest.fixture
def conn():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        yield connection
    finally:
        connection.rollback()
        connection.close()


def test_duplicate_asset_tag(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO assets (asset_tag, asset_type)
            VALUES (?, ?)
            """,
            ("PC-001", "PC"),
        )


def test_duplicate_serial_number(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO assets (asset_tag, asset_type, serial_number)
            VALUES (?, ?, ?)
            """,
            ("TEST-002", "PC", "SN-PC-001"),
        )


def test_invalid_priority(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO tickets (title, priority)
            VALUES (?, ?)
            """,
            ("Test invalid priority", "Urgent-Now"),
        )


def test_invalid_asset_reference(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO tickets (title, asset_id)
            VALUES (?, ?)
            """,
            ("Test invalid asset reference", -999),
        )
