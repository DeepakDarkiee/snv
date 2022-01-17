from accounts.models import User


class ContactAuthBackend:
    """Log in to Django without providing a password."""

    def authenticate(contact=None):
        try:
            return User.objects.get(contact=contact)
        except User.DoesNotExist:
            return None

    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
