from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta


class User(AbstractUser):
    """
    Класс модели пользователя
    """

    middle_name = models.CharField("Отчество", max_length=150, blank=True)
    email = models.EmailField("Адрес электронной почты", unique=True)  # переопределение
    # email с целью сделать это поле уникальным
    activation_key = models.CharField(max_length=50, blank=True)  # ключ для активации аккаунта
    activation_key_expires = models.DateTimeField(auto_now=True, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name",
                       "last_name",
                       ]

    def is_activation_key_expires(self):
        """
        Метод, который проверяет, попадает ли ввод ключа
        в установленный временной интервал
        return: Bool
        """

        if datetime.now() <= self.activation_key_expires + timedelta(hours=72):
            return False
        return True

    def __str__(self):
        return self.username

# Create your models here.
