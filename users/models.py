from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=50, verbose_name='Имя', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватарка', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email} - {self.first_name}'


class Payment(models.Model):
    class Method_payment(models.TextChoices):
        CASH = 'cash', 'Наличный расчет'
        TRANSFER = 'transfer', 'Перевод'

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.SET_NULL, related_name='payments', **NULLABLE)
    date_payment = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время платежа', **NULLABLE)
    method_payment = models.CharField(max_length=8, verbose_name="Способ оплаты", choices=Method_payment.choices,
                                      default=Method_payment.TRANSFER)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name="Оплаченный курс", **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name="Оплаченный урок", **NULLABLE)
    amount = models.PositiveIntegerField(default=0, verbose_name="Сумма платежа")
    session_id = models.CharField(max_length=255, verbose_name="Id сессии", **NULLABLE)
    link_payment = models.URLField(max_length=400, verbose_name="Ссылка на оплату", **NULLABLE)

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f'{self.amount}'
