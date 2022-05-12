from django.db import models
from uuid import uuid4


class Fees(models.Model):
    id          = models.UUIDField(primary_key=True,editable=False,default=uuid4)
    credit_fee  = models.CharField(max_length=125,null=False)
    debit_fee   = models.CharField(max_length=125,null=False)
    created_at  = models.DateTimeField(auto_now_add=True)
