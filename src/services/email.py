from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from src.config.settings import settings
import os

async def send_email(to_email: str, subject: str, content: str):
    message = Mail(
        from_email=settings.EMAIL_FROM,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    try:
        sg = SendGridAPIClient(settings.EMAIL_PASSWORD)
        response = sg.send(message)
        return response
    except Exception as e:
        print(e)
        raise
