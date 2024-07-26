from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from six import text_type

from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role', 'username']

    def create(self, validated_data):
        user = User.objects.create_user(
            name=validated_data['name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role')
        )
        return user

class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.name
        token['email'] = user.email
        token['role'] = user.role 

        return token

    def validate(self, attrs):
        data = super(UserTokenObtainPairSerializer, self).validate(attrs)

        refresh = self.get_token(self.user)
        data['refresh'] = text_type(refresh)
        data['access'] = text_type(refresh.access_token)
        data['name'] = self.user.name
        data['email'] = self.user.email
        data['role'] = self.user.role

        return data
