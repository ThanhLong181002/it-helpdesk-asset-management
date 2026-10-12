from db.connection import get_connection


def get_all_tickets():
    conn = get_connection()

    try:
        rows = conn.execute("""
            SELECT
                tickets.id,
                tickets.title,
                tickets.description,
                tickets.priority,
                tickets.status,
                tickets.created_at,
                tickets.resolved_at,
                assets.asset_tag,
                assets.asset_type,
                assets.assigned_to
            FROM tickets
            LEFT JOIN assets
                ON tickets.asset_id = assets.id
            ORDER BY
                CASE tickets.priority
                    WHEN 'Critical' THEN 1
                    WHEN 'High' THEN 2
                    WHEN 'Medium' THEN 3
                    WHEN 'Low' THEN 4
                END,
                tickets.created_at DESC
            """).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


def update_ticket_status(ticket_id, new_status, note=""):
    allowed_statuses = {
        "Open",
        "In Progress",
        "Resolved",
        "Closed",
    }

    if new_status not in allowed_statuses:
        raise ValueError("Invalid ticket status.")

    conn = get_connection()

    try:
        conn.execute("BEGIN")

        ticket = conn.execute(
            "SELECT status FROM tickets WHERE id = ?",
            (ticket_id,),
        ).fetchone()

        if ticket is None:
            raise ValueError(f"Ticket {ticket_id} does not exist.")

        old_status = ticket["status"]

        if old_status == new_status:
            conn.commit()
            return False

        conn.execute(
            """
            UPDATE tickets
            SET status = ?,
                resolved_at = CASE
                    WHEN ? = 'Resolved' THEN CURRENT_TIMESTAMP
                    WHEN ? = 'Closed' THEN COALESCE(
                        resolved_at, CURRENT_TIMESTAMP
                    )
                    ELSE NULL
                END
            WHERE id = ?
            """,
            (new_status, new_status, new_status, ticket_id),
        )

        conn.execute(
            """
            INSERT INTO ticket_history (
                ticket_id,
                old_status,
                new_status,
                note
            )
            VALUES (?, ?, ?, ?)
            """,
            (ticket_id, old_status, new_status, note),
        )

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def get_ticket_history(ticket_id):
    conn = get_connection()

    try:
        rows = conn.execute(
            """
            SELECT
                id,
                ticket_id,
                old_status,
                new_status,
                note,
                changed_at
            FROM ticket_history
            WHERE ticket_id = ?
            ORDER BY id DESC
            """,
            (ticket_id,),
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()
