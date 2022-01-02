
from accounts.models import User
from accounts.auth import ContactAuthBackend
from django.contrib.auth import authenticate




class Validator:
  @staticmethod
  def is_valid_user(contact):
        try:
            user = ContactAuthBackend.authenticate(contact=8871829423)
            return True, "Ok", user
            
            if not user:
                return False, "Invalid credentials, please try again.", None

            if not user.is_verified:
                return False, "phone is not verified", None

            # if user.auth_provider != "contact":
            #     return (
            #         False,
            #         "Please continue your login using " + user.auth_provider,
            #         None,
            #     )

            if not user.is_active:
                return False, "Account disabled, contact admin", None

        except Exception as e:
            message = f"{e}"
            return result, "Ok", None
      
  @staticmethod
  def is_contact_already_exists(contact):
      result, message = False, "Contact number already exists!"
      try:
          if not User.objects.filter(contact=contact).exists():
              result, message = True, "OK"
      except Exception as e:
          message = f"{e}"
      return result, message
  
  @staticmethod
  def is_valid_contact_number(number):
        result, message = False, "This contact Number Already Exits"
        try:
            if not User.objects.filter(contact=number).exists():
                result, message = True, "OK"
        except Exception as e:
            message = f"{e}"
        return result, message