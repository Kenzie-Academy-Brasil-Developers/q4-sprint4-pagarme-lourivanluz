from urllib.request import Request
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from datetime import datetime, date

from payment_info.models import PaymentInfo
from payment_info.serializers import PaymentInfoSerializer
from pagarme.permissions import IsBuyer
from users.models import Users


def isExpired(card_expiring_date):
    card_expiring_date = datetime.strptime(card_expiring_date, "%Y-%m-%d").date()
    return card_expiring_date >= date.today()


def format_card_number(card_number):
    return card_number[-4:]


class PaymentesInfoView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsBuyer]
    queryset = PaymentInfo.objects.all()
    serializer_class = PaymentInfoSerializer

    def create(self, request: Request):
        user: Users = request.user

        if not isExpired(request.data.get("card_expiring_date")):
            return Response({"error": ["This card is expired"]}, HTTP_400_BAD_REQUEST)
        serializer = PaymentInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        card_list = PaymentInfo.objects.filter(
            card_number=serializer.validated_data["card_number"],
            payment_method=serializer.validated_data["payment_method"],
        ).first()

        if not card_list:
            paymentInfo: PaymentInfo = PaymentInfo.objects.create(
                **serializer.validated_data
            )
            paymentInfo.customer = user
            paymentInfo.save()
            serializer = PaymentInfoSerializer(paymentInfo)
            response = serializer.data.copy()
            response["card_number_info"] = format_card_number(response["card_number"])
            response["customer"] = user.id

            return Response(response, HTTP_201_CREATED)
        return Response(
            {"error": ["This card is already registered for this user"]},
            HTTP_422_UNPROCESSABLE_ENTITY,
        )

    def list(self, request: Request):
        user: Users = request.user
        serializer = PaymentInfoSerializer(
            PaymentInfo.objects.filter(customer_id=user.id).all(), many=True
        )
        response = []
        for payment in serializer.data:
            paymentInfo = dict(payment).copy()
            paymentInfo["card_number"] = format_card_number(paymentInfo["card_number"])
            paymentInfo["customer"] = user.id
            response.append(paymentInfo)

        return Response(response, 200)
