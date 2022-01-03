from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(
        self,
        username,
        contact=None,
        first_name=None,
        auth_provider="email",
        is_verified=False,
        password=None,
        email=None,
    ):
        if username is None:
            raise TypeError("User should have a username")
        user = self.model(
            username=username,
            first_name=first_name,
            is_verified=is_verified,
            auth_provider=auth_provider,
            contact=contact,
            email=email,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        username,
        contact,
        first_name=None,
        auth_provider="email",
        is_verified=True,
        password=None,
    ):
        if password is None:
            raise TypeError("Password should not be None")

        user = self.create_user(
            username,
            contact,
            first_name=username,
            auth_provider="email",
            is_verified=True,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {"google": "google", "email": "email"}


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=15, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField()
    profile_pic = models.ImageField(blank=True, upload_to="profile_pics")
    auth_provider = models.CharField(
        max_length=255, blank=False, null=False, default="contact"
    )

    USERNAME_FIELD = "contact"
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
