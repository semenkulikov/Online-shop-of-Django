from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
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
        verbose_name='user'
    )
    fio = models.CharField(max_length=100, verbose_name='FIO')
    avatar_image = models.ImageField(
        upload_to='profile_avatars/',
        verbose_name='avatar'
    )
    phone_number = PhoneNumberField(
        blank=True,
        verbose_name='phone'
    )

    def __str__(self):
        return f'{self.fio} - {self.user.email}'

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
