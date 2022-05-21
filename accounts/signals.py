import string
import random
from django.db.models.signals import post_save
from django.dispatch import receiver

from gallery.models import Gallery
from accounts.models import User


@receiver(post_save, sender=User)
def create_gallery(sender, instance, created, **kwargs):
    if created:
        N = 5
        # generating random strings
        rand_string = "".join(
            random.choices(string.ascii_uppercase + string.ascii_lowercase, k=N)
        )

        name = instance.contact[:4] + "_" + rand_string
        Gallery.objects.create(user=instance, name=name)
        instance.save()
