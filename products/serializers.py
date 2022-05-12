from rest_framework import serializers


from products.models import Products
from users.serializers import UserResponse


class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            "id",
            "description",
            "price",
            "quantity",
            "is_active",
            "seller",
        ]

        extra_kwargs = {
            "is_active": {"read_only": True},
            "seller": {"read_only": True},
        }


class ProductDeteilsSerialiser(ProductsSerializers):
    seller = UserResponse(read_only=True)


class ProductPatch(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["id", "description", "price", "quantity", "is_active", "seller"]
        extra_kwargs = {
            "description": {"required": False},
            "price": {"required": False},
            "quantity": {"required": False},
            "is_active": {"required": False},
            "seller": {"required": False},
        }
