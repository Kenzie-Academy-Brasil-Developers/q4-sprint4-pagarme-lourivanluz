from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from fees.permissions import IsAdmim
from fees.models import Fees
from fees.serializers import FeesSerializer


class FeesView(generics.ListCreateAPIView):

    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated, IsAdmim]
    queryset = Fees.objects.all()
    serializer_class = FeesSerializer


class FeesViewId(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmim]
    queryset = Fees.objects.all()
    serializer_class = FeesSerializer
