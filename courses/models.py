from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса")
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True, verbose_name="Превью")
    description = models.TextField(verbose_name="Описание")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        'Course',  # Use a string reference here to avoid circular import issues
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Курс'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма'
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата платежа'
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'Платеж {self.id} от {self.user} за курс {self.course}'


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True, verbose_name="Превью")
    video_url = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Курс"
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Rating(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        unique_together = ('course', 'user')

    def __str__(self):
        return f'{self.course.title} - {self.score} от {self.user.username}'
