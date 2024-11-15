from django.db import models
from django.contrib.auth.models import User

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