from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework import status

from api.v1.users.serializers import UserTokenObtainPairSerializer, UserCreateSerializer


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def handle_exception(self, exc):
        if isinstance(exc, AuthenticationFailed):
            response_data = {
                "StatusCode": 6001,
                "message": {
                    "title": "Failed",
                    "body": "Username or Password invalid"
                },
                'error': str(exc.detail),
            }
            return Response(response_data, status=exc.status_code)
        return super().handle_exception(exc)
    

class UserCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
