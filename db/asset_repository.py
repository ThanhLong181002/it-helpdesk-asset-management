from db.connection import get_connection


def get_all_assets():
    conn = get_connection()

    try:
        rows = conn.execute("""
            SELECT
                id,
                asset_tag,
                asset_type,
                serial_number,
                assigned_to,
                location,
                status,
                created_at
            FROM assets
            ORDER BY asset_tag
            """).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()
