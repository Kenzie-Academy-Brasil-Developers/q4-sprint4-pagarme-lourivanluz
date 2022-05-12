from rest_framework import serializers


from users.models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','email','password','first_name','last_name','is_seller','is_admin']


class UserResponse(UserSerializer):
    class Meta:
        model = Users
        fields = ['id','email','first_name','last_name','is_seller','is_admin']


class LoginSerializer(serializers.Serializer):
    email           = serializers.CharField()
    password        = serializers.CharField()

