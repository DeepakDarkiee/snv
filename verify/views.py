from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from snv.common import app_logger, rest_utils

from verify.serializers import CreateSessionSerializer
from verify.repository import create_session


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
                        status.HTTP_201_CREATED, message, data=response_data, errors=None
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
