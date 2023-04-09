from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Класс модели пользователя
    """

    middle_name = models.CharField("Отчество", max_length=150, blank=True)
    avatar = models.ImageField("Аватар", upload_to="profiles")
    email = models.EmailField("Адрес электронной почты", unique=True)  # переопределение
    # email с целью сделать это поле уникальным

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

# Create your models here.
