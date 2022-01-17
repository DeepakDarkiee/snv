from django.conf import settings
from rest_framework import serializers
from snv.common.validations import Validator

from accounts.models import User
from accounts.utils import verify_contact_otp


class RegisterSerializer(serializers.ModelSerializer):
    contact = serializers.CharField(
        max_length=68, min_length=5, write_only=True, required=True
    )
    otp = serializers.IntegerField(write_only=True)

    # def create(self, validated_data):
    #     result, message, data = verify_contact_otp(validated_data)
    #     if not result:
    #         raise serializers.ValidationError(message)

    #     data = validated_data.pop("otp", None)
    #     return super().create(validated_data)

    class Meta:
        model = User
        fields = ["contact", "otp"]

    def validate(self, data):
        validated_data = {"otp": data["otp"], "contact": data["contact"]}
        result, message, data_otp = verify_contact_otp(validated_data)
        if not result:
            raise serializers.ValidationError(message)

        result, message = Validator.is_valid_contact_number(data["contact"])
        if not result:
            raise serializers.ValidationError(message)

        # if data["email"] != "":
        #     result, message = Validator.is_valid_exists_email(data["email"])
        #     if not result:
        #         raise serializers.ValidationError(message)

        return data


class OTPVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=555)
    contact = serializers.CharField(max_length=555)


class UserSendOptSerializer(serializers.Serializer):
    contact = serializers.CharField(
        max_length=68, min_length=5, write_only=True, required=True
    )

    # def validate(self, data):
    #     result, message = Validator.is_contact_already_exists(data["contact"])
    #     if not result:
    #         raise serializers.ValidationError(message)
    #     return data


class LoginSerializer(serializers.Serializer):
    contact = serializers.CharField(
        max_length=68, min_length=5, write_only=True, required=False
    )
    otp = serializers.IntegerField(write_only=True)

    tokens = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["tokens", "refresh_token", "contact", "otp"]

    def validate(self, attrs):
        contact = attrs.get("contact", None)
        otp = attrs.get("otp", None)
        user = User.objects.get(contact=contact)
        if user.is_active:
            validated_data = {"otp": otp, "contact": contact}
            otp_result, otp_message, data = verify_contact_otp(validated_data)
            if not otp_result:
                raise serializers.ValidationError(otp_message)
                return {
                    "message": otp_message,
                }
            else:
                result, message, user = Validator.is_valid_user(contact)
                if not result:
                    raise serializers.ValidationError(message)

                return {
                    "contact": user.contact,
                    "tokens": user.tokens().get("access"),
                    "refresh_token": user.tokens().get("refresh"),
                    "password": user.password,
                    "message": otp_message,
                }
        else:
            raise serializers.ValidationError("Your account is Deactivated")


class UpdateUserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            return f"{settings.URL}{obj.profile_pic.url}"
        else:
            return None

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "profile_pic",
        )


# class DeactivateUserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = (
#             "is_active",
#         )
