from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (RegisterView,SendUserOtp)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("user-send-otp/", SendUserOtp.as_view(), name="user-send-otp"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]