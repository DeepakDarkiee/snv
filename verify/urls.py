from django.urls import path

from verify.views import CreateSession, DocumentBackUpload, DocumentFrontUpload

urlpatterns = [
    path("create_session/", CreateSession.as_view(), name="create_session"),
    path(
        "front_document_upload/",
        DocumentFrontUpload.as_view(),
        name="front_document_upload",
    ),
    path(
        "back_document_upload/",
        DocumentBackUpload.as_view(),
        name="back_document_upload",
    ),
]
