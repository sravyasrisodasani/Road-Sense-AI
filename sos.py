import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

def format_number(number: str) -> str:
    """Auto-adds +91 for Indian numbers if no country code present."""
    number = number.strip().replace(" ", "").replace("-", "")
    if not number:
        return ""
    if not number.startswith("+"):
        number = "+91" + number
    return number

def send_sos(contacts: list, location: str, custom_message: str = None) -> dict:
    """
    Sends SOS SMS to multiple contacts via Twilio.
    Returns {"success": True/False, "sent": [...], "failed": [...]}
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token  = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")

    if not all([account_sid, auth_token, from_number]):
        return {"success": False, "error": "Twilio credentials missing in .env file."}

    formatted = [format_number(c) for c in contacts if c.strip()]
    if not formatted:
        return {"success": False, "error": "No valid contact numbers provided."}

    message_body = custom_message or (
        f"🚨 EMERGENCY ALERT 🚨\n"
        f"I need immediate help!\n"
        f"Location: {location}\n"
        f"Please call me or send help immediately.\n"
        f"- Sent via RoadSoS"
    )

    client = Client(account_sid, auth_token)
    sent = []
    failed = []

    for number in formatted:
        try:
            client.messages.create(body=message_body, from_=from_number, to=number)
            sent.append(number)
        except Exception as e:
            failed.append({"number": number, "error": str(e)})

    return {"success": len(sent) > 0, "sent": sent, "failed": failed}
