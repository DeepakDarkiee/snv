from django.urls import path

from verify.views import (
    CreateSession,
    DocumentBackUpload,
    DocumentFrontUpload,
    PersonFaceUpload,
    PersonQRCode,
    SNVerifiedPerson,
    VerificationDecision,
)

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
    path(
        "person_face_upload/",
        PersonFaceUpload.as_view(),
        name="person_face_upload",
    ),
    path(
        "decision/",
        VerificationDecision.as_view(),
        name="decision",
    ),
    path(
        "person/<str:session_id>/",
        SNVerifiedPerson.as_view(),
        name="person",
    ),
    path(
        "person_qr/",
        PersonQRCode.as_view(),
        name="person_qr",
    ),
]
