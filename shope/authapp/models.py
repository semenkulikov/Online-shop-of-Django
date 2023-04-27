from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
import pytz


class User(AbstractUser):
    """
    Класс модели пользователя
    """
    username = models.CharField("username", max_length=150,
                                null=True, blank=True)
    middle_name = models.CharField("middle name", max_length=150, blank=True)
    email = models.EmailField("email address", unique=True)  # переопределение
    # email с целью сделать это поле уникальным
    activation_key = models.CharField(max_length=50, blank=True)
    # ключ для активации аккаунта
    activation_key_expires = models.DateTimeField(auto_now=True,
                                                  blank=True,
                                                  null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    @property
    def is_activation_key_expires(self):
        """
        Метод, который проверяет, попадает ли ввод ключа
        в установленный временной интервал
        return: Bool
        """
        if datetime.now().replace(tzinfo=pytz.utc) \
                <= (self.activation_key_expires + timedelta(hours=72)):
            return False
        else:
            return True

    def __str__(self):
        return self.first_name + ' ' + self.last_name

# Create your models here.
