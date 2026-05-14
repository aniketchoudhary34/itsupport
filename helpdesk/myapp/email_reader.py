import imaplib
import email
from email.header import decode_header
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
from .models import taskdetails
import smtplib
from email.message import EmailMessage

# ---------- CONFIG FROM SETTINGS ----------
# READ EMAIL
IMAP_SERVER = settings.IMAP_SERVER
EMAIL_USER = settings.IMAP_EMAIL
EMAIL_PASS = settings.IMAP_PASSWORD

# SEND EMAIL
SMTP_SERVER = settings.EMAIL_HOST
SMTP_PORT = settings.EMAIL_PORT
SMTP_USER = settings.EMAIL_HOST_USER
SMTP_PASS = settings.EMAIL_HOST_PASSWORD

# ------------------------------------------

def fetch_tickets_from_email():
    # print("Connecting to email server...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    # print("Logged in successfully!")

    mail.select("inbox")
    status, messages = mail.search(None, '(UNSEEN SUBJECT "[TICKET]")')
    # print("Search Status:", status)
    # print("Emails found:", messages)

    if messages == [b'']:
        # print("No new ticket emails found.")
        return

    mail_ids = messages[0].split()
    for mail_id in mail_ids:
        _, msg_data = mail.fetch(mail_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # ---------- SUBJECT ----------
        subject, encoding = decode_header(msg["Subject"])[0]
        subject = subject.decode(encoding or "utf-8") if isinstance(subject, bytes) else subject
        title = subject.replace("[TICKET]", "").strip()
        # print("Email Subject (Title):", title)

        # ---------- FROM EMAIL ----------
        from_email = email.utils.parseaddr(msg.get("From"))[1]
        # print("From Email:", from_email)

        if not title:
            send_error_reply(msg, "Title missing")
            continue

        user, _ = User.objects.get_or_create(username=from_email, defaults={"email": from_email})

        # ---------- DESCRIPTION ----------
        description = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    description = part.get_payload(decode=True).decode(errors="ignore")
        else:
            description = msg.get_payload(decode=True).decode(errors="ignore")
        # print("Description length:", len(description))

        # ---------- CREATE TASK ----------
        task = taskdetails.objects.create(
            title=title,
            description=description,
            created_by=user,
            due_date=now().date() + timedelta(days=2)
        )
        # print(f"Task created: ID {task.id}, Title: {task.title}")

        # ---------- MARK AS READ ----------
        mail.store(mail_id, '+FLAGS', '\\Seen')

        # ---------- SEND SUCCESS EMAIL ----------
        send_success_reply(msg, task.id)

    mail.logout()
    # print("Email fetch complete.")


# ---------- EMAIL FUNCTIONS ----------
def send_mail(msg):
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            print("Mail sent to:", msg["To"])
    except Exception as e:
        print("Error sending mail:", e)


def send_success_reply(original_msg, ticket_id):
    reply = EmailMessage()
    reply["Subject"] = f"Ticket Created - #{ticket_id}"
    reply["From"] = SMTP_USER
    reply["To"] = email.utils.parseaddr(original_msg["From"])[1]
    reply.set_content(f"""
Your ticket has been created successfully.

Ticket ID: {ticket_id}
Status: New

IT Team will contact you.
""")
    send_mail(reply)


def send_error_reply(original_msg, reason):
    reply = EmailMessage()
    reply["Subject"] = "Ticket Request Failed"
    reply["From"] = SMTP_USER
    reply["To"] = email.utils.parseaddr(original_msg["From"])[1]
    reply.set_content(f"""
Your ticket request was not processed.

Reason:
{reason}

Please resend with subject:
[TICKET] Your issue title
""")
    send_mail(reply)
