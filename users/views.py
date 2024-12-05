<<<<<<< HEAD
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import filters, serializers
from users.models import User, Pay
from users.serializer import UserSerializer, PaySerializer
from users.services import create_stripe_session, create_stripe_product, create_stripe_price


class PayViewSet(ModelViewSet):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('payed_course', 'payed_lesson', 'type_of_payment')
    ordering_fields = ('date',)


class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get('password'))
        user.save()


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveApiView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyApiView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PayListAPIView(ListAPIView):
    """Просмотр списка платежей с фильтрацией по курсу, уроку и способу оплаты,
       и с сортировкой по дате(по умолчанию в модели сортировка по убыванию,
       при запросе можно изменить с помощью -"""
    serializer_class = PaySerializer
    queryset = Pay.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('payed_course', 'payed_lesson', 'type_of_payment')
    ordering_fields = ('date',)


class PayCreateAPIView(CreateAPIView):
    serializer_class = PaySerializer
    queryset = Pay.objects.all()

    def perform_create(self, serializer):
        pay = serializer.save(user=self.request.user)
        product = create_stripe_product(product_name='new product')
        price = create_stripe_price(product, pay.summ)
        session_id, payment_link = create_stripe_session(price)

        pay.session_id = session_id
        pay.link = payment_link
        pay.save()


=======
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserRegistrationView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> 189608c909cf437c2d8bfea0aafa445bf4172ede
