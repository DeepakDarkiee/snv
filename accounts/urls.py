from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    DeactivateUserAccount,
    LoginAPIView,
    RegisterView,
    SendUserOtp,
    UserProfileUpdate,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("user-send-otp/", SendUserOtp.as_view(), name="user-send-otp"),
    path(
        "user-profile-update/",
        UserProfileUpdate.as_view(),
        name="user-profile-update",
    ),
    path(
        "deactivate-user-account/",
        DeactivateUserAccount.as_view(),
        name="deactivate-user-account",
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
