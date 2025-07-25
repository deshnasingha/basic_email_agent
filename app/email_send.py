from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization, To, Bcc, Email
from app.db.schemas.responses import APIResponse, StatusEnum
from app.core.config import SENDGRID_API_KEY


sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)

def send(toaddr, subject, body):
    to = toaddr
    from_email = "deshnasingha@umass.edu"
    content = body
    subject = subject

    message = Mail(
        from_email = from_email,
        to_emails = to,
        subject = subject,
        plain_text_content = content
    )

    try:
        response = sg.send(message)
        
        if response.status_code == 202:
            return APIResponse(
                status = StatusEnum.SUCCESS,
                detailed_message ="Email sent successfully"
            )

    except Exception as e:
        return APIResponse(
            status = StatusEnum.FAIL,
            error_message = str(e),
            detailed_message = "Failed to send email"
        )
