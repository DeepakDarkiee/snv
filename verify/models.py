from accounts.models import User
from django.db import models


# Create your models here.
class Verification(models.Model):
    session_id = models.CharField(max_length=255, null=True, blank=True)
    document_front = models.ImageField(upload_to="document", null=True, blank=True)
    document_back = models.ImageField(upload_to="document", null=True, blank=True)
    photo = models.ImageField(upload_to="document", null=True, blank=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="verification",
        null=True,
        blank=True,
    )
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.contact
