from drf_yasg.utils import swagger_serializer_method
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from snv.common import app_logger, rest_utils

from accounts.models import User
from accounts.permissions import IsLogin
from accounts.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UpdateUserSerializer,
    UserSendOptSerializer,
)

from .utils import create_user, user_message_send

logger = app_logger.createLogger("app")

# Create your views here.


class SendUserOtp(generics.GenericAPIView):
    serializer_class = UserSendOptSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                result, message, response_data = user_message_send(
                    request.data["contact"]
                )
                if result:
                    return rest_utils.build_response(
                        status.HTTP_200_OK, message, data=serializer.data, errors=None
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


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):

        try:
            data = request.data
            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                user = serializer.save(contact=data.get("contact"), is_verified=True)
                result, message, response_data = create_user(user, data)
                if result:
                    data = serializer.data
                    data["token"] = user.tokens().get("access")
                    data["refresh_token"] = user.tokens().get("refresh")
                    return rest_utils.build_response(
                        status.HTTP_200_OK, message, data=data, errors=None
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


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                message = "User Successfully Login"
                return rest_utils.build_response(
                    status.HTTP_200_OK, message, data=serializer.data, errors=None
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


class UserProfileUpdate(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
    parser_classes = (MultiPartParser,)

    @swagger_serializer_method(serializer_or_field=UpdateUserSerializer)
    def put(self, request, format=None):
        try:
            # user = User.objects.get(pk=pk)
            serializer = self.serializer_class(request.user, data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                return rest_utils.build_response(
                    status.HTTP_200_OK,
                    "User Profile Updated",
                    data=serializer.data,
                    errors=None,
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


class DeactivateUserAccount(generics.GenericAPIView):

    permission_classes = (IsLogin,)

    def put(self, request, format=None):
        try:
            user = User.objects.get(id=request.user.id)
            user.is_active = False
            user.save()
            return rest_utils.build_response(
                status.HTTP_200_OK,
                "User Deactivated",
                errors=None,
            )
            # else:
            #     return rest_utils.build_response(
            #         status.HTTP_400_BAD_REQUEST,
            #         rest_utils.HTTP_REST_MESSAGES["400"],
            #         data=None,
            #         errors=serializer.errors,
            #     )

        except Exception as e:
            message = rest_utils.HTTP_REST_MESSAGES["500"]
            return rest_utils.build_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR, message, data=None, errors=str(e)
            )
