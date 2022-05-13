from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from datetime import timedelta


from fees.models import Fees
from payables.models import Payable
from payables.serializer import PayablesSerializer
from transactions.models import Order, Transaction
from users.models import Users
from products.models import Products
from payment_info.models import PaymentInfo
from transactions.serializers import TransactionsSerializer
from payment_info.views import isExpired
from transactions.permissions import IsBuyerOrAdm


class TransactionsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsBuyerOrAdm]

    def post(self, request: Request):

        seller = request.data["seller"]["id"]
        products = request.data["seller"]["products"]
        payment_info = request.data["payment_info"]["id"]

        payment_card: PaymentInfo = PaymentInfo.objects.filter(id=payment_info).first()
        if not isExpired(str(payment_card.card_expiring_date)):
            return Response({"error": ["This card is expired"]}, 400)

        error = []   
        if payment_card.customer.id != request.user.id:
            return Response({"error": "ta clonando pq ?"}, 400)

        transactions: Transaction = Transaction.objects.create(
            payment_info_id=payment_info, seller_id=seller
        )

        seller: Users = Users.objects.filter(id=seller).first()
        if not seller:
            return Response(
                {"error": ["All products must belong to the same seller"]}, 400
            )
        # ver melhor forma, ou ver antes de fazer a ordem ou depois
        # se depois verificar a melhor forma de retornar o erro.
        value = 0
        for product in products:
            product_filtred: Products = Products.objects.filter(
                id=product["id"]
            ).first()
            if not product_filtred:
                return Response({"error": "nao existe product"}, 400)
            if product_filtred.quantity < product["quantity"]:
                return Response({"error": "quantidade menor"}, 400)
            if not product_filtred.is_active:
                return Response({"error": "produto nao esta ativo"}, 400)

            Order.objects.create(
                quantity=product["quantity"],
                amount=product_filtred.price * product["quantity"],
                transaction=transactions,
                product=product_filtred,
            )
            product_filtred.quantity -= product["quantity"]
            product_filtred.save()
            value += product_filtred.price * product["quantity"]

        transactions.amount = value
        transactions.save()

        fee: Fees = Fees.objects.last()

        payable_obj = (
            {
                "status": "waiting_funds",
                "payment_date": transactions.created_at + timedelta(days=30),
                "amount": transactions.amount - float(fee.credit_fee) * 100,
            }
            if payment_card.payment_method == "credit"
            else {
                "status": "paid",
                "payment_date": transactions.created_at,
                "amount": transactions.amount - float(fee.debit_fee) * 100,
            }
        )

        payable = Payable.objects.create(
            **payable_obj, transaction=transactions, fee=fee, seller=seller
        )

        serializer = PayablesSerializer(payable)

        return Response(serializer.data, 200)

    def get(self, request: Request):
        payables = Payable.objects.all()
        if request.user.is_seller:
            payables = payables.filter(seller_id=request.user.id).all()
        serializer = PayablesSerializer(payables, many=True)

        return Response(serializer.data, 200)
