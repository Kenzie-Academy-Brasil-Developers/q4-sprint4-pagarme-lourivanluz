from django.db import models
from uuid import uuid4


class PaymentInfo(models.Model):

    id                  = models.UUIDField(primary_key=True,editable=False,default=uuid4)
    payment_method      = models.CharField(max_length=255,null=False)
    card_number         = models.CharField(max_length=255,null=False)
    cardholders_name    = models.CharField(max_length=255,null=False)
    card_expiring_date  = models.DateField(null=False)
    cvv                 = models.CharField(max_length=255,null=False)
    is_active           = models.BooleanField(default=True)

    customer            = models.ForeignKey('users.Users',related_name='paymentInfos',on_delete=models.CASCADE,null=True)