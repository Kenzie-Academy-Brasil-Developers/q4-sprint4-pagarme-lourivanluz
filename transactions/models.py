from django.db import models
from uuid import uuid4


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    amount = models.FloatField(null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)

    payment_info = models.ForeignKey(
        "payment_info.PaymentInfo",
        on_delete=models.CASCADE,
        related_name="transactions",
        null=True,
    )

    seller = models.ForeignKey(
        "users.Users", on_delete=models.CASCADE, related_name="transactions", null=True
    )


class Order(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    quantity = models.IntegerField(null=False)
    amount = models.IntegerField(null=False)

    transaction = models.ForeignKey(
        "transactions.Transaction",
        on_delete=models.CASCADE,
        related_name="orders",
    )

    product = models.ForeignKey("products.Products", on_delete=models.CASCADE)
