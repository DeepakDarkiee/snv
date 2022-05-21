from django.shortcuts import render
from drf_yasg.utils import swagger_serializer_method
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from snv.common import app_logger, rest_utils

from verify.models import Verification
from verify.repository import (
    back_document_upload,
    create_session,
    front_document_upload,
    get_decision,
    get_person,
    get_qr,
    person_face_upload,
)
from verify.serializers import (
    BackDocumentUploadSerializer,
    CreateSessionSerializer,
    FrontDocumentUploadSerializer,
    PersonFaceUploadSerializer,
)


# Create your views here.
class CreateSession(generics.GenericAPIView):
    serializer_class = CreateSessionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = request.data
                user = request.user
                result, message, response_data = create_session(data)
                session_id = response_data.get("id")
                verification_object, created = Verification.objects.get_or_create(
                    user=request.user,
                )
                if not verification_object.session_id:
                    verification_object.session_id = session_id
                    verification_object.save()
                if result:
                    return rest_utils.build_response(
                        status.HTTP_201_CREATED,
                        message,
                        data=response_data,
                        errors=None,
                    )
                else:
                    return rest_utils.build_response(
                        status.HTTP_400_BAD_REQUEST, message, data=None, errors=message
                    )
            else:
                return rest_utils.build_response(
                    status.HTTP_400_BAD_REQUEST,
                    rest_utils.HTTP_REST_MESSAGES["400"],
                    data=None,
                    errors=serializer.errors,
                )

        except Exception as e:
            message = rest_utils.HTTP_REST_MESSAGES["500"]
            return rest_utils.build_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR, message, data=None, errors=str(e)
            )


class DocumentFrontUpload(generics.GenericAPIView):
    serializer_class = FrontDocumentUploadSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    @swagger_serializer_method(serializer_or_field=FrontDocumentUploadSerializer)
    def put(self, request, format=None):
        try:
            instance = Verification.objects.get(user=request.user)
            serializer = self.serializer_class(
                instance, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                document_front = serializer.data["document_front"]

                data = {
                    "content": document_front,
                    "context": "document-front",
                    "timestamp": "2019-10-29T06:30:25.597Z",
                    "user": request.user,
                }
                result, message, response_data = front_document_upload(data)
                if result:
                    return rest_utils.build_response(
                        status.HTTP_201_CREATED,
                        message,
                        data=response_data,
                        errors=None,
                    )
                else:
                    return rest_utils.build_response(
                        status.HTTP_400_BAD_REQUEST,
                        message,
                        data=None,
                        errors=message,
                    )
            else:
                return rest_utils.build_response(
                    status.HTTP_400_BAD_REQUEST,
                    rest_utils.HTTP_REST_MESSAGES["400"],
                    data=None,
                    errors=serializer.errors,
                )

        except Exception as e:
            message = rest_utils.HTTP_REST_MESSAGES["500"]
            return rest_utils.build_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR, message, data=None, errors=str(e)
            )


class DocumentBackUpload(generics.GenericAPIView):
    serializer_class = BackDocumentUploadSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    @swagger_serializer_method(serializer_or_field=FrontDocumentUploadSerializer)
    def put(self, request, format=None):
        try:
            instance = Verification.objects.get(user=request.user)
            serializer = self.serializer_class(
                instance, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                document_back = serializer.data["document_back"]
                data = {
                    "content": document_back,
                    "context": "document-back",
                    "timestamp": "2019-10-29T06:30:25.597Z",
                    "user": request.user,
                }
                result, message, response_data = back_document_upload(data)
                if result:
                    return rest_utils.build_response(
                        status.HTTP_201_CREATED,
                        message,
                        data=response_data,
                        errors=None,
                    )
                else:
                    return rest_utils.build_response(
                        status.HTTP_400_BAD_REQUEST,
                        message,
                        data=None,
                        errors=message,
                    )
            else:
                return rest_utils.build_response(
                    status.HTTP_400_BAD_REQUEST,
                    rest_utils.HTTP_REST_MESSAGES["400"],
                    data=None,
                    errors=serializer.errors,
                )

        except Exception as e:
            message = rest_utils.HTTP_REST_MESSAGES["500"]
            return rest_utils.build_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR, message, data=None, errors=str(e)
            )


class PersonFaceUpload(generics.GenericAPIView):
    serializer_class = PersonFaceUploadSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    @swagger_serializer_method(serializer_or_field=FrontDocumentUploadSerializer)
    def put(self, request, format=None):
        try:
            instance = Verification.objects.get(user=request.user)
            serializer = self.serializer_class(
                instance, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                face = serializer.data["photo"]
                data = {
                    "content": face,
                    "context": "face",
                    "timestamp": "2019-10-29T06:30:25.597Z",
                    "user": request.user,
                }
                result, message, response_data = person_face_upload(data)
                if result:
                    return rest_utils.build_response(
                        status.HTTP_201_CREATED,
                        message,
                        data=response_data,
                        errors=None,
                    )
                else:
                    return rest_utils.build_response(
                        status.HTTP_400_BAD_REQUEST,
                        message,
                        data=None,
                        errors=message,
                    )
            else:
                return rest_utils.build_response(
                    status.HTTP_400_BAD_REQUEST,
                    rest_utils.HTTP_REST_MESSAGES["400"],
                    data=None,
                    errors=serializer.errors,
                )

        except Exception as e:
            message = rest_utils.HTTP_REST_MESSAGES["500"]
            return rest_utils.build_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR, message, data=None, errors=str(e)
            )


class VerificationDecision(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            user = request.user
            result, message, response_data = get_decision(user)
            return rest_utils.build_response(
                status.HTTP_200_OK,
                message=message,
                data=response_data,
                errors=None,
            )

        except Exception as e:
            message = rest_utils.HTTP_REST_MESSAGES["500"]
            return rest_utils.build_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR, message, data=None, errors=str(e)
            )


class SNVerifiedPerson(generics.GenericAPIView):
    
    def get(self, request, session_id, format=None):
        try:
            result, message, response_data = get_person(session_id)
            return rest_utils.build_response(
                status.HTTP_200_OK,
                message=message,
                data=response_data,
                errors=None,
            )

        except Exception as e:
            message = rest_utils.HTTP_REST_MESSAGES["500"]
            return rest_utils.build_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR, message, data=None, errors=str(e)
            )


class PersonQRCode(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            user = request.user
            result, message, response_data = get_qr(user)
            return rest_utils.build_response(
                status.HTTP_200_OK,
                message=message,
                data=response_data,
                errors=None,
            )

        except Exception as e:
            message = rest_utils.HTTP_REST_MESSAGES["500"]
            return rest_utils.build_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR, message, data=None, errors=str(e)
            )
