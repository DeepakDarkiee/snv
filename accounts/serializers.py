from rest_framework import serializers
from accounts.models import User
from accounts.utils import verify_contact_otp


class RegisterSerializer(serializers.ModelSerializer):
    contact = serializers.CharField(
        max_length=68, min_length=5, write_only=True, required=False
    )
    otp = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        result, message, data = verify_contact_otp(validated_data)
        if not result:
            raise serializers.ValidationError(message)

        data = validated_data.pop("otp", None)
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ["contact", "otp"]

    # def validate(self, data):

    # result, message = Validator.is_valid_gender(data["gender"])
    # if not result:
    #     raise serializers.ValidationError(message)

    # result, message = Validator.is_valid_contact_number(data["contact"])result, message = Validator.is_valid_gender(data["gender"])
    # if not result:
    #     raise serializers.ValidationError(message)

    # result, message = Validator.is_valid_contact_number(data["contact"])
    # if not result:
    #     raise serializers.ValidationError(message)

    # if data["email"] != "":
    #     result, message = Validator.is_valid_exists_email(data["email"])
    #     if not result:
    #         raise serializers.ValidationError(message)

    # return data


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