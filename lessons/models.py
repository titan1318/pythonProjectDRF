from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    image = models.ImageField(upload_to='lessons/courses', verbose_name='изображение', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField(verbose_name='Цена', **NULLABLE)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='lessons/lessons', verbose_name='изображение', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='курс', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    video_url = models.URLField(max_length=300, verbose_name="Видео урока", **NULLABLE)
    price = models.IntegerField(verbose_name='Цена', **NULLABLE)


    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Subscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='subscription_user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс',
                               related_name='subscription_course')
    is_subscribe = models.BooleanField(default=False, verbose_name="подписка")

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

