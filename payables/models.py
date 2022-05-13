from django.db import models


from uuid import uuid4


class Payable(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    status = models.CharField(max_length=125, null=False)
    payment_date = models.DateTimeField(null=False)
    amount = models.FloatField(null=False)

    transaction = models.OneToOneField(
        "transactions.Transaction", on_delete=models.CASCADE
    )
    fee = models.ForeignKey("fees.Fees", on_delete=models.CASCADE)
    seller = models.ForeignKey(
        "users.Users", on_delete=models.CASCADE, related_name="payables"
    )


""" status = waiting_funds
payment_date = data da transação + 30 dias
amount_client = valor da transação - taxa relativa ao cartão de crédito.

status = paid
payment_date = data da transação
amount_client = valor da transação - taxa relativa ao cartão de débito. """
