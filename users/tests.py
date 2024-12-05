<<<<<<< HEAD

=======
from django.test import TestCase
<<<<<<< HEAD
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
=======
>>>>>>> 189608c909cf437c2d8bfea0aafa445bf4172ede
>>>>>>> 9ff2f24294ef21ce0325f374f0cc082d46302804


class UserViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_user_login(self):
        response = self.client.post('/api/token/', {"username": "testuser", "password": "testpassword"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
