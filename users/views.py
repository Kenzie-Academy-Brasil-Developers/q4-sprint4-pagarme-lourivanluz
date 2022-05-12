from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


from users.serializers import LoginSerializer, UserSerializer, UserResponse
from users.models import Users
from pagarme.permissions import IsAdmim


class UsersView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmim]
    queryset = Users.objects.all()
    serializer_class = UserResponse

    def list(self, _: Request):
        serializer = UserResponse(Users.objects.all(), many=True)
        return Response(serializer.data, HTTP_200_OK)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["password"] = make_password(
            serializer.validated_data["password"]
        )
        user: Users = Users.objects.create(**serializer.validated_data)
        if user.is_admin:
            user.is_seller = False
            user.save()
        serializer = UserResponse(user)
        return Response(serializer.data, HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: Users = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if not user:
            return Response({"detail": "unauthorized."}, HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, HTTP_200_OK)
