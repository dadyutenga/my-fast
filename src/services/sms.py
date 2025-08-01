from twilio.rest import Client
from src.config.settings import settings

async def send_sms(to_number: str, body: str):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=body,
            from_=settings.TWILIO_FROM_NUMBER,
            to=to_number
        )
        return message.sid
    except Exception as e:
        print(e)
        raise
