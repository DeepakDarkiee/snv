from django.db import models


# Create your models here.
class Verification(models.Model):
    session_id = models.CharField(max_length=255, null=True, blank=True)
    document_front = models.ImageField(upload_to="document", null=True, blank=True)
    document_back = models.ImageField(upload_to="document", null=True, blank=True)
    photo = models.ImageField(upload_to="document", null=True, blank=True)
