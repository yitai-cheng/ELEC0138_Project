from twilio.rest import Client
from django.conf import settings
import random
import base64
def generate_verification_code():
    return str(random.randint(100000, 999999))
def send_verification_code(to_phone_number, code):
    print(to_phone_number)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verification = client.verify \
        .services(settings.TWILIO_VERIFY_SERVICE_SID) \
        .verifications \
        .create(to=to_phone_number, channel='sms')
    return verification.sid

def check_verification_code(phone_number, user_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verification_check = client.verify \
        .services(settings.TWILIO_VERIFY_SERVICE_SID) \
        .verification_checks \
        .create(to=phone_number, code=user_code)

    return verification_check.status == 'approved'
