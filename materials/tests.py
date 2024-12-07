from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from materials.models import Course, Lesson, Subscription


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.course = Course.objects.create(title='course-title', description='course-description', owner=self.user)
        self.lesson = Lesson.objects.create(title='lesson-title', description='lesson-description', course=self.course,
                                            owner=self.user)
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """ Тестирование просмотра одного курса """
        url = reverse('materials:courses-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        result = {
            'title': self.course.title,
            'preview': None,
            'description': self.course.description,
            'owner': self.user.pk,
            'count_lessons': 1,
            'lessons': [
                {
                    'id': self.lesson.pk,
                    'linc_to_video': None,
                    'title': self.lesson.title,
                    'preview': None,
                    'description': self.lesson.description,
                    'course': self.course.pk,
                    'owner': self.user.pk
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            data.get('title'), self.course.title
        )
        # self.maxDiff = None
        self.assertEqual(
            data, result
        )

    def test_course_list(self):
        """ Тестирование просмотра списка курсов """
        url = reverse('materials:courses-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.course.pk,
                    'is_subscribed': True,
                    'title': self.course.title,
                    'preview': None,
                    'description': self.course.description,
                    'owner': self.user.pk
                }
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            data, result
        )

    def test_course_create(self):
        """ Тестирование создания курса """
        url = reverse('materials:courses-list')
        data = {
            'title': 'test-title'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        """ Тестирование редактирование курса """
        url = reverse('materials:courses-detail', args=(self.course.pk,))
        data = {
            'title': 'test-title'
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.get('title'), 'test-title'
        )

    def test_course_delete(self):
        """ Тестирование удаление курса """
        url = reverse('materials:courses-detail', args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Course.objects.all().count(), 0
        )


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.course = Course.objects.create(title='course-title', description='course-description', owner=self.user)
        self.lesson = Lesson.objects.create(title='lesson-title', description='lesson-description', course=self.course,
                                            owner=self.user)
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        """ Тестирование создания урока """
        url = reverse('materials:lesson-create')
        data = {
            'title': 'test-title',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        """ Тестирование редактирование урока """
        url = reverse('materials:lesson-update', args=(self.lesson.pk,))
        data = {
            'title': 'test-title'
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.get('title'), 'test-title'
        )

    def test_lesson_delete(self):
        """ Тестирование удаление урока """
        url = reverse('materials:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_detail(self):
        """ Тестирование просмотра одного урока """
        url = reverse('materials:lesson-detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        result = {
            'id': self.lesson.pk,
            'linc_to_video': None,
            'title': self.lesson.title,
            'preview': None,
            'description': self.lesson.description,
            'course': self.course.pk,
            'owner': self.user.pk
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            data, result
        )

    def test_lesson_list(self):
        """ Тестирование просмотра списка уроков """
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.lesson.pk,
                    'linc_to_video': None,
                    'title': self.lesson.title,
                    'preview': None,
                    'description': self.lesson.description,
                    'course': self.course.pk,
                    'owner': self.user.pk
                }
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            data, result
        )

class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.course = Course.objects.create(title='course-title', description='course-description', owner=self.user)

        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        """ Тестирование функционала работы подписки на курс"""
        url = reverse('materials:subscription-create')
        data = {
            'course_id': self.course.pk,
        }
        # Добавление подписки на курс self.course
        response = self.client.post(url, data)
        data_1 = response.json()
        result_1 = {'message': 'Подписка добавлена'}

        # Удаление подписки на курс self.course
        response = self.client.post(url, data)
        data_2 = response.json()
        result_2 = {'message': 'Подписка удалена'}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data_1, result_1
        )
        self.assertEqual(
            data_2, result_2
        )



