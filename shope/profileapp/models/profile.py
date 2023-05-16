from django.db import models
from authapp.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    """
    Profile models.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='user'
    )
    fio = models.CharField(
        max_length=100,
        verbose_name='FIO'
    )

    avatar_image = models.ImageField(
        upload_to='profile_avatars/',
        verbose_name='avatar',
        null=True,
        blank=True
    )

    phone_number = PhoneNumberField(
        blank=True,
        unique=True,
        verbose_name='phone number'
    )

    def __str__(self):
        return f'{self.fio} - {self.user.email}'

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
