from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from snv.common import app_logger, rest_utils

from verify.models import Verification
from verify.repository import (
    back_document_upload,
    create_session,
    front_document_upload,
)
from verify.serializers import (
    BackDocumentUploadSerializer,
    CreateSessionSerializer,
    FrontDocumentUploadSerializer,
)


# Create your views here.
class CreateSession(generics.GenericAPIView):
    serializer_class = CreateSessionSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = request.data
                result, message, response_data = create_session(data)
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
    parser_classes = (MultiPartParser,)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                document_front = serializer.data["document_front"]

                data = {
                    "content": document_front,
                    "context": "document-front",
                    "timestamp": "2019-10-29T06:30:25.597Z",
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
    parser_classes = (MultiPartParser,)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                document_back = serializer.data["document_back"]
                data = {
                    "content": document_back,
                    "context": "document-back",
                    "timestamp": "2019-10-29T06:30:25.597Z",
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
