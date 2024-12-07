from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import Payment, User
from users.permissions import IsUser
from users.serializers import PaymentSerializer, UserSerializer, UserNotOwnerSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class UserCreateAPIView(CreateAPIView):
    """Создать пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """Список пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    """Профиль пользователя"""
    queryset = User.objects.all()

    def get_serializer_class(self):
        """Если запрашивается свой профиль, используем полный сериализатор, иначе сокращенный сериализатор."""
        if self.request.user == self.get_object():
            return UserSerializer
        else:
            return UserNotOwnerSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Изменить пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsUser)


class UserDestroyAPIView(DestroyAPIView):
    """Удалить пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsUser)


class PaymentViewSet(viewsets.ModelViewSet):
    """Позволяет автоматически реализовать стандартные методы CRUD для модели Payment"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method_payment',)
    ordering_fields = ("date_payment",)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_id = create_stripe_product(payment)
        price = create_stripe_price(payment.amount, product_id)
        session_id, link_payment = create_stripe_session(price)
        payment.session_id = session_id
        payment.link_payment = link_payment
        payment.save()

# class PaymentListAPIView(generics.ListAPIView):
#     serializer_class = PaymentSerializer
#     queryset = Payment.objects.all()
#     filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
#     filterset_fields = ('course', 'lesson', 'method_payment',)
#     ordering_fields = ('date',)
#
#
# class PaymentCreateAPIView(generics.CreateAPIView):
#     serializer_class = PaymentSerializer
#     queryset = Payment.objects.all()
#
#     def perform_create(self, serializer):
#         payment = serializer.save(user=self.request.user)
#         product_id = create_stripe_product(payment)
#         price = create_stripe_price(payment.amount, product_id)
#         session_id, payment_link = create_stripe_session(price)
#         payment.session_id = session_id
#         payment.link_payment = payment_link
#         payment.save()
