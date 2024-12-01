from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='www@yandex.com')
        self.course = Course.objects.create(name='Основы Английского', description='научитесь грамотно говорить в любой стране')
        self.lesson = Lesson.objects.create(name='жи-ши с буквой и', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        url = reverse('lessons:lesson_create')
        data = {
            'name': 'А теперь граматика',
            'description': 'крутой урок, бесспорно',
            'course': self.course.pk,
            'owner': self.user.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_Youtube_valid(self):
        url = reverse('lessons:lesson_create')
        data = {
            'name': 'Урок на YouTube',
            'description': 'Полезный урок',
            'course': self.course.pk,
            'owner': self.user.pk,
            'video_url': 'https://www.youtube.com/watch?v=example'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_Youtube_invalid(self):
        url = reverse('lessons:lesson_create')
        data = {
            'name': 'Неверная ссылка',
            'description': 'Урок с неверной ссылкой',
            'course': self.course.pk,
            'owner': self.user.pk,
            'video_url': 'https://www.example.com/'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_lesson_retrieve(self):
        url = reverse('lessons:lesson_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update(self):
        url = reverse('lessons:lesson_update', args=(self.lesson.pk,))
        data = {
            'name': 'Обновлённый урок',
            'description': 'Обновленное описание',
            'course': self.course.pk,
            'owner': self.user.pk
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Обновлённый урок')

    def test_lesson_delete(self):
        url = reverse('lessons:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse('lessons:lesson_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='www@yandex.com')
        self.course = Course.objects.create(name='Основы Английского', description='научитесь грамотно говорить в любой стране')
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        Subscription.objects.all().delete()
        url = reverse('lessons:subscription_create')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Вы подписались')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        url = reverse('lessons:subscription_create')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Вы отписались')

    def test_subscription_list(self):
        url = reverse('lessons:subscription_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['course'], self.course.id)

    def test_subscribe_to_nonexistent_course(self):
        Subscription.objects.all().delete()
        url = reverse('lessons:subscription_create')
        data = {'course_id': 9999}  # Несуществующий курс
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscribe_without_authentication(self):
        self.client.force_authenticate(user=None)
        url = reverse('lessons:subscription_create')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

