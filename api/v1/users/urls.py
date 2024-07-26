from .views import UserCreateView, UserTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from django.urls import path


app_name = 'api_v1_users'

urlpatterns = [
    path('token/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateView.as_view(), name='user_register'),
]

