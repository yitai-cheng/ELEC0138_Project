from twilio.rest import Client
from django.conf import settings
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
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
def generate_RSA_keys():

    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key.decode(), public_key.decode()

def encrypt_RSA(public_key, message):

    recipient_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    ciphertext = cipher_rsa.encrypt(message.encode())
    return base64.b64encode(ciphertext).decode()

def decrypt_RSA(private_key, ciphertext):

    key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(key)
    decrypted_message = cipher_rsa.decrypt(base64.b64decode(ciphertext.encode())).decode()
    return decrypted_message