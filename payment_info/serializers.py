from rest_framework.serializers import ModelSerializer


from payment_info.models import PaymentInfo

class PaymentInfoSerializer(ModelSerializer):
    class Meta:
        model   = PaymentInfo
        fields  = [
            'id','payment_method','card_number','cardholders_name',
            'card_expiring_date','cvv','is_active'
            ]
        extra_kwargs = {'cvv': {'write_only': True}}
