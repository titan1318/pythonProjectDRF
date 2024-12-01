from django.urls import path
<<<<<<< HEAD
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PayViewSet, UserListApiView, UserRetrieveApiView, UserCreateApiView, UserDestroyApiView, \
    UserUpdateApiView, PayListAPIView, PayCreateAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register('', PayViewSet)

urlpatterns = [
    path('user/', UserListApiView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserRetrieveApiView.as_view(), name='user_retrieve'),
    path('register/', UserCreateApiView.as_view(), name='register'),
    path('user/<int:pk>/delete/', UserDestroyApiView.as_view(), name='user_delete'),
    path('user/<int:pk>/update/', UserUpdateApiView.as_view(), name='user_update'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path("payment/", PayListAPIView.as_view(), name="payment_list"),
    path("payment_create/", PayCreateAPIView.as_view(), name="payment_create"),
=======
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
>>>>>>> 189608c909cf437c2d8bfea0aafa445bf4172ede
]

urlpatterns += router.urls
