from datetime import datetime

tickets = {}


def create_ticket(ticket_id):
    tickets[ticket_id] = {
        "status": "not_started",

        "assign": False,
        "pending": False,
        "greeting": False,
        "com": False,
        "done_comment": False,
        "hours": None,
        "done_done": False,

        "done_comment_type": None,
        "notes": [],

        "created_at": datetime.now(),
        "completed_at": None,

        "message_id": None,
        "channel_id": None
    }


def progress(ticket):
    steps = [
        bool(ticket.get("assign")),
        bool(ticket.get("pending")),
        bool(ticket.get("greeting")),
        bool(ticket.get("com")),
        bool(ticket.get("done_comment")),
        bool(ticket.get("hours")),
        bool(ticket.get("done_done")),
    ]

    return int(sum(steps) / len(steps) * 100)