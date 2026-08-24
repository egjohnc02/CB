import sqlite3
import json
import os
from datetime import datetime


DB_PATH = os.path.join(os.path.dirname(__file__), "tickets.db")
tickets = {}


# ============================================================
# DATABASE INITIALIZATION & SYNC
# ============================================================

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            status TEXT,
            assign INTEGER,
            pending INTEGER,
            greeting INTEGER,
            com INTEGER,
            done_comment INTEGER,
            hours INTEGER,
            done_done INTEGER,
            ticket_type TEXT,
            done_comment_type TEXT,
            language TEXT,
            notes TEXT,
            created_at TEXT,
            completed_at TEXT,
            message_id INTEGER,
            channel_id INTEGER
        )
    """)
    conn.commit()

    # Load all existing tickets into memory
    cursor.execute("SELECT * FROM tickets")
    rows = cursor.fetchall()

    for row in rows:
        tid = row["ticket_id"]
        created_at = datetime.fromisoformat(row["created_at"]) if row["created_at"] else datetime.now()
        completed_at = datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None

        notes = []
        if row["notes"]:
            try:
                notes = json.loads(row["notes"])
            except Exception:
                notes = []

        tickets[tid] = {
            "status": row["status"] or "not_started",
            "assign": bool(row["assign"]),
            "pending": bool(row["pending"]),
            "greeting": bool(row["greeting"]),
            "com": bool(row["com"]),
            "done_comment": bool(row["done_comment"]),
            "hours": bool(row["hours"]),
            "done_done": bool(row["done_done"]),
            "ticket_type": row["ticket_type"],
            "done_comment_type": row["done_comment_type"],
            "language": row["language"],
            "notes": notes,
            "created_at": created_at,
            "completed_at": completed_at,
            "message_id": row["message_id"],
            "channel_id": row["channel_id"],
        }

    conn.close()
    print(f"📦 [DATABASE] Loaded {len(tickets)} tickets from {DB_PATH}")


def save_ticket(ticket_id):
    ticket_id = find_ticket_id(ticket_id)
    ticket = tickets.get(ticket_id)
    if not ticket:
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    created_at_str = ticket["created_at"].isoformat() if ticket.get("created_at") else None
    completed_at_str = ticket["completed_at"].isoformat() if ticket.get("completed_at") else None
    notes_str = json.dumps(ticket.get("notes", []))

    cursor.execute("""
        INSERT OR REPLACE INTO tickets (
            ticket_id, status, assign, pending, greeting, com,
            done_comment, hours, done_done, ticket_type,
            done_comment_type, language, notes, created_at,
            completed_at, message_id, channel_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket_id,
        ticket.get("status", "not_started"),
        int(bool(ticket.get("assign"))),
        int(bool(ticket.get("pending"))),
        int(bool(ticket.get("greeting"))),
        int(bool(ticket.get("com"))),
        int(bool(ticket.get("done_comment"))),
        int(bool(ticket.get("hours"))),
        int(bool(ticket.get("done_done"))),
        ticket.get("ticket_type"),
        ticket.get("done_comment_type"),
        ticket.get("language"),
        notes_str,
        created_at_str,
        completed_at_str,
        ticket.get("message_id"),
        ticket.get("channel_id"),
    ))

    conn.commit()
    conn.close()


# ============================================================
# TICKET LOOKUP & CRUD
# ============================================================

def find_ticket_id(query):
    if not query:
        return ""
    q = str(query).strip().upper()
    if q in tickets:
        return q
    if f"ENRICH-{q}" in tickets:
        return f"ENRICH-{q}"
    for tid in tickets:
        if tid.endswith(f"-{q}") or tid == q:
            return tid
    return q


def create_ticket(ticket_id):
    ticket_id = str(ticket_id).strip().upper()
    tickets[ticket_id] = {
        "status": "not_started",

        "assign": False,
        "pending": False,
        "greeting": False,
        "com": False,
        "done_comment": False,
        "hours": False,
        "done_done": False,

        "ticket_type": None,  # "do", "cancel", "on_hold"
        "done_comment_type": None,
        "language": None,

        "notes": [],

        "created_at": datetime.now(),
        "completed_at": None,

        "message_id": None,
        "channel_id": None,
    }
    save_ticket(ticket_id)
    return ticket_id


def get_ticket(ticket_id):
    resolved = find_ticket_id(ticket_id)
    return tickets.get(resolved)


def ticket_exists(ticket_id):
    resolved = find_ticket_id(ticket_id)
    return resolved in tickets


def delete_ticket(ticket_id):
    resolved = find_ticket_id(ticket_id)
    if resolved in tickets:
        del tickets[resolved]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tickets WHERE ticket_id = ?", (resolved,))
        conn.commit()
        conn.close()
        return True
    return False


def reopen_ticket(ticket_id):
    resolved = find_ticket_id(ticket_id)
    ticket = tickets.get(resolved)
    if not ticket:
        return False

    ticket["status"] = "in_progress"
    ticket["done_done"] = False
    ticket["completed_at"] = None
    save_ticket(resolved)
    return True


def resume_ticket(ticket_id):
    resolved = find_ticket_id(ticket_id)
    ticket = tickets.get(resolved)
    if not ticket:
        return False

    ticket["status"] = "in_progress"
    ticket["done_comment"] = False
    ticket["ticket_type"] = None
    ticket["done_done"] = False
    save_ticket(resolved)
    return True


def add_note(ticket_id, note_text):
    resolved = find_ticket_id(ticket_id)
    ticket = tickets.get(resolved)
    if not ticket:
        return False

    if "notes" not in ticket:
        ticket["notes"] = []

    ticket["notes"].append(note_text)
    save_ticket(resolved)
    return True


# Automatically initialize DB on import
init_db()