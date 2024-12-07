from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserDestroyAPIView, UserUpdateAPIView, \
    PaymentViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'payment', PaymentViewSet, basename='payment')

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path("users/", UserListAPIView.as_view(), name="users"),
    path("user/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_retrieve"),
    path("user/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("user/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user_retrieve"),

    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),

] + router.urls
