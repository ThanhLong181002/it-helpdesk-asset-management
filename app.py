from flask import Flask, render_template, request, redirect, url_for, flash


from db.connection import get_connection
from db.asset_repository import get_all_assets


from db.ticket_repository import (
    get_all_tickets,
    update_ticket_status,
    get_ticket_history,
)

app = Flask(__name__)

app.secret_key = "long-scret-key"


@app.route("/")
def home():
    conn = get_connection()

    try:
        total_assets = conn.execute("SELECT COUNT(*) FROM assets").fetchone()[0]

        open_tickets = conn.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE status IN ('Open', 'In Progress')
            """).fetchone()[0]

        resolved_tickets = conn.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE status = 'Resolved'
            """).fetchone()[0]

    finally:
        conn.close()

    recent_tickets = get_all_tickets()[:5]

    return render_template(
        "dashboard.html",
        total_assets=total_assets,
        open_tickets=open_tickets,
        resolved_tickets=resolved_tickets,
        recent_tickets=recent_tickets,
    )


@app.route("/assets")
def assets_page():
    assets = get_all_assets()
    return render_template("assets.html", assets=assets)


@app.route("/tickets")
def tickets_page():
    tickets = get_all_tickets()

    selected_status = request.args.get("status", "")
    selected_priority = request.args.get("priority", "")

    allowed_statuses = {
        "Open",
        "In Progress",
        "Resolved",
        "Closed",
    }

    allowed_priorities = {
        "Low",
        "Medium",
        "High",
        "Critical",
    }

    if selected_status not in allowed_statuses:
        selected_status = ""

    if selected_priority not in allowed_priorities:
        selected_priority = ""

    if selected_status:
        tickets = [ticket for ticket in tickets if ticket["status"] == selected_status]

    if selected_priority:
        tickets = [
            ticket for ticket in tickets if ticket["priority"] == selected_priority
        ]

    return render_template(
        "tickets.html",
        tickets=tickets,
        selected_status=selected_status,
        selected_priority=selected_priority,
    )


@app.route("/tickets/<int:ticket_id>/update", methods=["POST"])
def update_ticket(ticket_id):
    new_status = request.form.get("status", "")
    note = request.form.get("note", "").strip()

    try:
        changed = update_ticket_status(ticket_id, new_status, note)

        if changed:
            flash(f"Ticket #{ticket_id} status updated successfully.", "success")
        else:
            flash(f"Ticket #{ticket_id} already has that status.", "info")

    except ValueError as error:
        flash(str(error), "danger")

    return redirect(url_for("tickets_page"))


@app.route("/tickets/<int:ticket_id>")
def ticket_detail(ticket_id):
    conn = get_connection()

    try:
        row = conn.execute(
            """
            SELECT
                tickets.id,
                tickets.title,
                tickets.description,
                tickets.priority,
                tickets.status,
                tickets.created_at,
                tickets.resolved_at,
                assets.asset_tag,
                assets.assigned_to
            FROM tickets
            LEFT JOIN assets
                ON tickets.asset_id = assets.id
            WHERE tickets.id = ?
            """,
            (ticket_id,),
        ).fetchone()

        if row is None:
            return render_template("404.html"), 404

        ticket = dict(row)

    finally:
        conn.close()

    history = get_ticket_history(ticket_id)

    return render_template(
        "ticket_detail.html",
        ticket=ticket,
        history=history,
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
