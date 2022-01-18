from rest_framework import serializers


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
    timestamp = serializers.CharField(max_length=30)
