from django.db import models
from uuid import uuid4


class Products(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    description = models.CharField(max_length=255, null=False)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    is_active = models.BooleanField(default=True)

    seller = models.ForeignKey(
        "users.Users", on_delete=models.CASCADE, related_name="products"
    )
