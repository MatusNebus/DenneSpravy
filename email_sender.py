# email_sender.py
from __future__ import annotations

import os
import re
import html
import smtplib
from pathlib import Path
from email.message import EmailMessage


def digest_to_html(digest_text: str) -> str:
    """
    Prevedie digest (plain text) do jednoduchého HTML:
    - riadky typu '1.[NÁZOV UDALOSTI]' dá do <strong>
    - zachová nové riadky cez <br>
    - text escapuje, aby sa nerozbilo HTML
    """
    lines = digest_text.splitlines()
    out: list[str] = []

    for raw in lines:
        line = raw.rstrip("\n")
        if not line.strip():
            out.append("<br>")
            continue

        safe = html.escape(line)

        # Nadpisy položiek: "1. ..." / "1) ..." / prípadne "[...]"
        if re.match(r"^\s*([1-5][\.\)]\s+.+|\[.+\])\s*$", line):
            out.append(f"<strong>{safe}</strong><br>")
        else:
            out.append(f"{safe}<br>")

    return "".join(out)


def load_recipients() -> list[str]:
    """
    Primárne: načíta z config/recipients.txt (tento súbor príde z private repo checkoutu v Actions).
    Fallback: EMAIL_RECIPIENTS z env (aby to fungovalo aj kým private repo ešte nie je zapojené).
    """
    # 1) Private-config cesta (po checkout-e v workflow)
    config_path = Path("config") / "recipients.txt"
    if config_path.exists():
        lines = config_path.read_text(encoding="utf-8").splitlines()
        recips = [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]
        if recips:
            return recips

    # 2) Fallback na env
    recipients_raw = os.getenv("EMAIL_RECIPIENTS", "")
    return [r.strip() for r in recipients_raw.split(",") if r.strip()]


def send_email(subject: str, body: str) -> None:
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    sender_email = os.getenv("EMAIL_SENDER")
    email_password = os.getenv("EMAIL_PASSWORD")

    recipients = load_recipients()
    if not recipients:
        raise RuntimeError(
            "Chýbajú príjemcovia: pridaj config/recipients.txt (private repo) "
            "alebo nastav EMAIL_RECIPIENTS."
        )

    if not sender_email or not email_password:
        raise RuntimeError("Chýbajú EMAIL_SENDER alebo EMAIL_PASSWORD v env.")

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    # plain text
    msg.set_content(body)

    # html
    html_body = f"""\
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.5;">
    {digest_to_html(body)}
  </body>
</html>
"""
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(sender_email, email_password)
        server.send_message(msg)
