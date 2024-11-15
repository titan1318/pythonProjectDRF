from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Course, Rating
from rest_framework.exceptions import ValidationError
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import RatingSerializer



class CourseAPITestCase(APITestCase):

    def setUp(self):
        # Создаём суперпользователя
        self.admin_user = User.objects.create_superuser(
            username='admin', password='admin123', email='admin@example.com'
        )
        self.client = APIClient()

        # Получаем токен и устанавливаем его
        token = AccessToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Создаём тестовый курс
        self.course = Course.objects.create(
            title="Тестовый курс", description="Описание курса", creator=self.admin_user
        )

    def test_get_courses(self):
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course(self):
        data = {
            "title": "Новый курс",
            "description": "Описание нового курса",
        }
        response = self.client.post('/api/courses/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_course(self):
        data = {
            "title": "Обновленный курс",
            "description": "Обновленное описание",
        }
        response = self.client.put(f'/api/courses/{self.course.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_course(self):
        response = self.client.delete(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class RatingAPITestCase(APITestCase):

    def setUp(self):
        # Создаем пользователей и курс
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')
        self.client = APIClient()

        self.course = Course.objects.create(title="Тестовый курс", description="Описание курса", creator=self.admin_user)

    def test_create_rating(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'course': self.course.id,
            'score': 5
        }
        response = self.client.post('/api/ratings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)

    def test_unique_rating_per_user(self):
        self.client.login(username='testuser', password='password123')
        data = {'course': self.course.id, 'score': 4}
        self.client.post('/api/ratings/', data)
        response = self.client.post('/api/ratings/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Ожидаем ошибку из-за уникального ограничения

    def test_get_average_rating(self):
        Rating.objects.create(course=self.course, user=self.user, score=5)
        Rating.objects.create(course=self.course, user=self.admin_user, score=3)
        self.client.login(username='testuser', password='password123')
        response = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['average_rating'], 4.0)  # Среднее значение

class RatingAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.course = Course.objects.create(title="Тестовый курс", description="Описание курса")
        self.client.force_authenticate(user=self.user)

    def test_create_rating(self):
        data = {"course": self.course.id, "score": 4}
        response = self.client.post('/api/ratings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unique_rating_per_user(self):
        Rating.objects.create(course=self.course, user=self.user, score=4)
        data = {"course": self.course.id, "score": 5}
        response = self.client.post('/api/ratings/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        course = serializer.validated_data['course']
        if Rating.objects.filter(user=user, course=course).exists():
            raise ValidationError("You have already rated this course.")
        serializer.save(user=user)