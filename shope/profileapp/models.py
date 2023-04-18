from django.db import models

from authapp.models import User


class Profile(models.Model):
    """
    Profile models.
    Пока номер телефона так. Потом переделать с регуляркой и валидатором.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='пользователь'
    )
    fio = models.CharField(max_length=100, verbose_name='ФИО')
    avatar_image = models.ImageField(
        upload_to='profile_avatars/',
        verbose_name='аватар'
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name='номер телефона'
    )

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
