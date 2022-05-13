from rest_framework import generics
from rest_framework.request import Request
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
)


from pagarme.permissions import IsSeller
from products.serializers import (
    ProductsSerializers,
    ProductDeteilsSerialiser,
    ProductPatch,
)
from users.models import Users
from users.serializers import UserResponse
from products.models import Products


class ProductView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSeller]

    def post(self, request: Request):
        user: Users = request.user

        serialiser = ProductDeteilsSerialiser(data=request.data)
        serialiser.is_valid(raise_exception=True)

        if request.data.get("price") < 0 or request.data.get("quantity") < 0:
            return Response({"msg": "invalid"}, HTTP_400_BAD_REQUEST)

        serialiser.validated_data["seller"] = user
        product = Products.objects.create(**serialiser.validated_data)

        serialiser = ProductDeteilsSerialiser(product)

        serialiser.data["seller"] = UserResponse(
            Users.objects.filter(email=user.email).first()
        ).data

        return Response(serialiser.data, HTTP_201_CREATED)

    def get(self, _: Request):
        serialiser = ProductsSerializers(
            Products.objects.filter(is_active=True).all(), many=True
        )
        return Response(serialiser.data, HTTP_200_OK)


class ProductGetPatchView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSeller]

    def get(self, _: Request, product_id):
        products = Products.objects.filter(id=product_id)
        if not products.first():
            return Response({"message": "products does not exist"}, HTTP_404_NOT_FOUND)
        serialiser = ProductsSerializers(products.first())
        return Response(serialiser.data, HTTP_200_OK)

    def patch(self, request: Request, product_id):
        user: Users = request.user

        if (
            request.data.get("price")
            and request.data.get("price") < 0
            or request.data.get("quantity")
            and request.data.get("quantity") < 0
        ):
            return Response({"msg": "invalid"}, HTTP_400_BAD_REQUEST)

        products = Products.objects.filter(id=product_id)
        if not products.first():
            return Response({"message": "products does not exist"}, HTTP_404_NOT_FOUND)

        produ: Products = products.first()
        if produ.seller.id == user.id:

            serializer = ProductPatch(request.data)
            products.update(**serializer.data)
            serializer = ProductPatch(products.first())

            return Response(serializer.data, HTTP_200_OK)

        return Response(
            {"detail": "Authentication credentials were not provided."},
            HTTP_401_UNAUTHORIZED,
        )


class ProductListSellerId(generics.ListAPIView):
    def get(self, _: Request, seller_id):

        seller: Users = Users.objects.filter(id=seller_id).first()
        if not seller:
            return Response({"detail": "Not found."}, HTTP_404_NOT_FOUND)

        serialiser = ProductsSerializers(
            Products.objects.filter(seller_id=seller_id).all(), many=True
        )
        return Response(serialiser.data, HTTP_200_OK)
