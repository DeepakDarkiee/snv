from django.db import models

# Create your models here.
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        username=None,
        contact=None,
        first_name=None,
        last_name = None,
        auth_provider="contact",
        is_verified=False,
        password=None,
    ):
        if email is None:
            raise TypeError("User should have a email")
        user = self.model(
            username=username,
            first_name=first_name,
            last_name = last_name,
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
        contact,
        email,
        username=None,
        first_name=None,
        last_name=None,
        auth_provider="contact",
        is_verified=True,
        password=None,
    ):
        if password is None:
            raise TypeError("Password should not be None")

        user = self.create_user(
            email,
            username,
            contact,
            first_name=first_name,
            last_name=last_name,
            auth_provider="email",
            is_verified=True,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user




class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, db_index=True,null=True,blank=True)
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(max_length=255, default="", null=True, blank=True,db_index=True)
    contact = models.CharField(max_length=15, null=True, blank=True,unique=True)
    profile_pic = models.ImageField(blank=True, upload_to="profile_pics")
    is_verified = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=255, blank=False, null=False, default="contact"
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["contact"]
    objects = UserManager()

    def __str__(self):
        return str(self.contact)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}