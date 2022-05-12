from rest_framework.serializers import ModelSerializer


from fees.models import Fees

class FeesSerializer(ModelSerializer):
    class Meta:
        model = Fees
        fields = '__all__'