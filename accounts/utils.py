from accounts.models import User
from django.conf import settings
from django.contrib.auth import authenticate
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
verify = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID)

def create_user(user, request_data):
    result, message, data = False, "Failed", None
    try:
        # user.set_password(request_data.get("password"))
        user = user.save()
        # send user contact OTP
        result, message, data = True, "User created successfully", None
    except Exception as e:
        result, message, data = False, str(e), None
    return result, message, data

def user_check_otp(phone, code):
    try:
        verify_status = client.verify.services(
            settings.TWILIO_VERIFY_SERVICE_SID
        ).verification_checks.create(to="+91" + phone, code=code)
        return verify_status.status == "approved"
    except TwilioRestException as e:
        return False

def verify_contact_otp(request_data):
    result, message, data = False, "Failed", None
    phone = request_data.get("contact", None)
    otp = request_data.get("otp", None)
    # user = User.objects.get(contact=phone)
    verify = user_check_otp(phone, otp)
    if verify:
        # user.is_verified = True
        # user.save()
        result, message, data = True, "Successfully Verified", None
    else:
        result, message, data = False, "Invalid OTP", None
    return result, message, data
  
  
def user_message_send(phone):
    try:
        client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID).verifications.create(
            to="+91" + phone, channel="sms"
        )
        result, message, data = True, "User OTP successfully send", None
    except Exception as e:
        result, message, data = False, str(e), None
    return result, message, data