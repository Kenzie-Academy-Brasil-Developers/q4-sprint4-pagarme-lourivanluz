from rest_framework import serializers


class TransactionsSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    amount = serializers.FloatField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
