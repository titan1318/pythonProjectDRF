from django.db import models

from config.settings import AUTH_USER_MODEL

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(upload_to='course/preview', verbose_name="Превью", **NULLABLE)
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец курса", **NULLABLE)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f'{self.title}'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(upload_to='lesson/preview', verbose_name="Превью", **NULLABLE)
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    linc_to_video = models.URLField(max_length=150, verbose_name="Ссылка на видео", **NULLABLE)
    course = models.ForeignKey(Course, verbose_name="Курс", on_delete=models.CASCADE, null=True, related_name="lessons")
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец курса", **NULLABLE)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f'{self.title}'


class Subscription(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь",
                             related_name='subs_user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс",
                               related_name='subs_course')

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f'{self.user} - {self.course}'
