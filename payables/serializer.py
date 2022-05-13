from rest_framework import serializers


class PayablesSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    amount = serializers.CharField()
