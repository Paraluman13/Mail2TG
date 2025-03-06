import imaplib
import email
import requests
import time

EMAIL_USER = ""
EMAIL_PASS = ""
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def fetch_emails():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        status, messages = mail.search(None, 'UNSEEN SUBJECT "TESTING BOT"')
        email_ids = messages[0].split()

        print(f"Found {len(email_ids)} unread emails.")

        for e_id in email_ids:
            _, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg["subject"]
                    sender = msg["from"]
                    body = ""

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    print(f"Email from {sender}, Subject: {subject}, Body: {body}")
                    send_to_telegram(f"📩 *New Email Received*\n\n*From:* {sender}\n*Subject:* {subject}\n\n{body}")

        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

def send_to_telegram(message):
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    response = requests.post(TELEGRAM_URL, data=payload)
    if response.status_code == 200:
        print("Message sent to Telegram")
    else:
        print(f"Failed to send message: {response.text}")

if __name__ == "__main__":
    while True:
        fetch_emails()
        time.sleep(60)
