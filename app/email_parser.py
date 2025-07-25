import email
from email import policy
from email.parser import BytesParser

def parse_email(raw_email_bytes: bytes):
    msg = BytesParser(policy=policy.default).parsebytes(raw_email_bytes)

    sender = msg['from']
    subject = msg['subject']

    # Get the email body (handle multipart or plain text)
    # for now just looking at text/plain content
    if msg.is_multipart():
        parts = msg.walk()
        body = ""
        for part in parts:
            if part.get_content_type() == "text/plain":
                body += part.get_content()
    else:
        body = msg.get_content()

    return sender, subject, body