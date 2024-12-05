from rest_framework import viewsets
from .serializers import PaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import create_stripe_product, create_stripe_price, create_stripe_session, retrieve_stripe_session
from .models import Payment
from django.shortcuts import get_object_or_404
from courses.models import Course



class StripePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        # Создаем продукт в Stripe
        product = create_stripe_product(course.title)
        # Цена указывается в копейках
        price = create_stripe_price(product['id'], int(course.price * 100))
        # Создаем сессию для оплаты
        session = create_stripe_session(price['id'])

        # Сохраняем ссылку на оплату в нашей системе
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            stripe_session_id=session['id'],
            amount=course.price,
            status='created'
        )

        return Response({"url": session['url']})


class StripeSessionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        session_id = request.query_params.get('session_id')
        session = retrieve_stripe_session(session_id)
        return Response({"status": session['payment_status']})


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
