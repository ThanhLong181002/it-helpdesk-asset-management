from app import app


def test_dashboard_returns_success():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"IT Helpdesk Dashboard" in response.data


def test_assets_page_returns_success():
    response = app.test_client().get("/assets")

    assert response.status_code == 200
    assert b"Asset Management" in response.data


def test_tickets_page_returns_success():
    response = app.test_client().get("/tickets")

    assert response.status_code == 200
    assert b"Support Tickets" in response.data


def test_ticket_detail_returns_success():
    response = app.test_client().get("/tickets/1")

    assert response.status_code == 200
    assert b"PC cannot connect to network" in response.data


def test_missing_ticket_returns_custom_404():
    response = app.test_client().get("/tickets/9999")

    assert response.status_code == 404
    assert b"Page Not Found" in response.data


def test_invalid_status_filter_is_ignored():
    response = app.test_client().get("/tickets?status=InvalidStatus")

    assert response.status_code == 200
    assert b"3 tickets" in response.data


def test_invalid_priority_filter_is_ignored():
    response = app.test_client().get("/tickets?priority=Urgent")

    assert response.status_code == 200
    assert b"3 tickets" in response.data
