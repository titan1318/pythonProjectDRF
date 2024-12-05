from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from ..courses.models import Course
from ..courses.serializers import CourseSerializer
from django.contrib.auth.models import User




class CourseSerializerTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title="Test Course", description="Test Description")

    def test_course_serialization(self):
        serializer = CourseSerializer(self.course)
        self.assertEqual(serializer.data['title'], "Test Course")


class CourseViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(
            title="Тестовый курс",
            description="Описание тестового курса",
            creator=self.user
        )

    def test_get_courses(self):
        response = self.client.get("/courses/")
        self.assertEqual(response.status_code, 200)


class CourseModelTest(TestCase):
    def setUp(self):
        # Создаем пользователя для поля ForeignKey
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(
            title="Тестовый курс",
            description="Описание тестового курса",
            creator=self.user  # Предполагаем, что поле ForeignKey называется `creator`
        )

    def test_course_creation(self):
        self.assertEqual(self.course.title, "Тестовый курс")
        self.assertEqual(self.course.description, "Описание тестового курса")
        self.assertEqual(self.course.creator, self.user)
