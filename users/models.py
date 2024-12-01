from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from lessons.models import Lesson, Course

NULLABLE = {'blank': True, 'null': True}


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создаёт и возвращает пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError("У пользователя должен быть указан email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создаёт и возвращает суперпользователя с указанным email и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Отключаем поле username
    email = models.EmailField(
        verbose_name='почта',
        unique=True
    )
    phone = models.CharField(max_length=55, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/avatars', verbose_name='аватар', **NULLABLE)
    city = models.CharField(max_length=55, verbose_name='город', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Pay(models.Model):
    pay_type = (
        ('Cash', "наличные"),
        ('Card', "перевод "),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    payed_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    payed_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    summ = models.IntegerField(verbose_name='Сумма')
    type_of_payment = models.CharField(choices=pay_type, verbose_name="Способ Оплаты")

    session_id = models.CharField(max_length=255, verbose_name='Id сессии', **NULLABLE)
    link = models.URLField(max_length=400, verbose_name='Cсылка на оплату', **NULLABLE)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж пользователя {self.user.email}"
