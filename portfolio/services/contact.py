"""Validated, rate-limited contact intake with optional SMTP delivery."""

from __future__ import annotations

import os
import re
import smtplib
import sqlite3
import ssl
import time
from collections import defaultdict, deque
from email.message import EmailMessage
from html import escape
from threading import Lock


EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
WINDOW_SECONDS = 15 * 60
MAX_MESSAGES = 5
_attempts: dict[str, deque[float]] = defaultdict(deque)
_lock = Lock()


class ContactError(ValueError):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


def _clean(value: object, maximum: int) -> str:
    return " ".join(str(value or "").strip().split())[:maximum]


def _check_rate_limit(key: str) -> None:
    now = time.time()
    with _lock:
        queue = _attempts[key or "unknown"]
        while queue and queue[0] < now - WINDOW_SECONDS:
            queue.popleft()
        if len(queue) >= MAX_MESSAGES:
            raise ContactError("Too many messages. Please try again in a few minutes.", 429)
        queue.append(now)


def _save(database: str, name: str, email: str, subject: str, message: str) -> int:
    with sqlite3.connect(database) as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        cursor = connection.execute(
            "INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)",
            (name, email, subject, message),
        )
        connection.commit()
        return int(cursor.lastrowid)


def _send_email(name: str, email: str, subject: str, message: str) -> bool:
    host = os.getenv("SMTP_HOST")
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    recipient = os.getenv("CONTACT_TO_EMAIL")
    if not all((host, username, password, recipient)):
        return False

    mail = EmailMessage()
    mail["Subject"] = f"Portfolio: {subject}"
    mail["From"] = username
    mail["To"] = recipient
    mail["Reply-To"] = email
    mail.set_content(f"From: {name} <{email}>\n\n{message}")
    context = ssl.create_default_context()
    with smtplib.SMTP(host, int(os.getenv("SMTP_PORT", "587")), timeout=12) as server:
        server.starttls(context=context)
        server.login(username, password)
        server.send_message(mail)
    return True


def accept_message(payload: dict, database: str, remote_addr: str) -> dict:
    if payload.get("company_website"):
        return {"message": "Message received.", "delivered": False}

    _check_rate_limit(remote_addr)
    name = _clean(payload.get("name"), 80)
    email = _clean(payload.get("email"), 160).lower()
    subject = _clean(payload.get("subject") or "Portfolio enquiry", 120)
    message = _clean(payload.get("message"), 3000)

    if len(name) < 2:
        raise ContactError("Please enter your full name.")
    if not EMAIL_RE.fullmatch(email):
        raise ContactError("Please enter a valid email address.")
    if len(message) < 15:
        raise ContactError("Please add a little more detail to your message.")

    message_id = _save(database, escape(name), email, escape(subject), escape(message))
    delivered = False
    try:
        delivered = _send_email(name, email, subject, message)
    except (OSError, smtplib.SMTPException):
        # The enquiry is already stored, so an email outage never loses it.
        delivered = False

    return {
        "message": "Thanks — your message has been received.",
        "reference": f"MSG-{message_id:05d}",
        "delivered": delivered,
    }
