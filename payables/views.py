from unittest import result
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.request import Request
from rest_framework.response import Response


from payables.permissions import IsSeller
from payables.models import Payable


class PayablesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSeller]

    def get(self, request: Request):
        payables: list[Payable] = Payable.objects.filter(
            seller_id=request.user.id
        ).all()

        paid = sum([payable for payable in payables if payable.status == "paid"])
        waiting_funds = sum(
            [payable for payable in payables if payable.status == "waiting_funds"]
        )
        result = {
            "payable_amount_paid": paid,
            "payable_amount_waiting_funds": waiting_funds,
        }
        return Response(result, 200)
