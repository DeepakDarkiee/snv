from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from verify.models import Verification


class CreateSessionSerializer(serializers.Serializer):
    # person: object
    firstName = serializers.CharField(max_length=100)
    lastName = serializers.CharField(max_length=100)
    idNumber = serializers.CharField(max_length=100)

    # document: object
    number = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=40)
    type = serializers.CharField(max_length=20)

    # additionalData: object
    vendorData = serializers.CharField(max_length=40)
    timestamp = serializers.DateTimeField(default=timezone.now(), read_only=True)


class FrontDocumentUploadSerializer(serializers.ModelSerializer):

    context = serializers.CharField(
        max_length=100, default="document-front", read_only=True
    )
    timestamp = serializers.DateTimeField(initial=timezone.now(), read_only=True)

    class Meta:
        model = Verification
        fields = ("document_front", "context", "timestamp")


class BackDocumentUploadSerializer(serializers.ModelSerializer):

    context = serializers.CharField(
        max_length=100, default="document-back", read_only=True
    )
    timestamp = serializers.DateTimeField(initial=timezone.now(), read_only=True)

    class Meta:
        model = Verification
        fields = ("document_back", "context", "timestamp")


class PersonFaceUploadSerializer(serializers.ModelSerializer):

    context = serializers.CharField(max_length=100, default="face", read_only=True)
    timestamp = serializers.DateTimeField(initial=timezone.now(), read_only=True)

    class Meta:
        model = Verification
        fields = ("photo", "context", "timestamp")
