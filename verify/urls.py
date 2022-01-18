from django.urls import path

from verify.views import CreateSession

urlpatterns = [
    path("create_session/", CreateSession.as_view(), name="create_session"),
]
