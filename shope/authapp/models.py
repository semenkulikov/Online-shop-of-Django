from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Класс модели пользователя
    """
    middle_name = models.CharField("Отчество", max_length=150, blank=True)
    avatar = models.ImageField("Аватар", upload_to="profiles")

    def __str__(self):
        return self.username

# Create your models here.
