from django.test import TestCase
from rest_framework.test import APITestCase
from payments.models import Payment
from rest_framework import status
from django.contrib.auth.models import User


class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(
            title="Тестовый курс",
            description="Описание тестового курса",
            creator=self.user
        )
        self.payment = Payment.objects.create(
            user=self.user,
            course=self.course,
            amount=100.0,
            status="SUCCESS"
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.amount, 100.0)
        self.assertEqual(self.payment.status, "SUCCESS")
        self.assertEqual(self.payment.user, self.user)
        self.assertEqual(self.payment.course, self.course)


class PaymentViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(
            title="Тестовый курс",
            description="Описание тестового курса",
            creator=self.user
        )
        self.payment = Payment.objects.create(
            user=self.user,
            course=self.course,
            amount=100.0,
            status="SUCCESS"
        )

    def test_get_payments(self):
        response = self.client.get("/payments/")
        self.assertEqual(response.status_code, 200)
