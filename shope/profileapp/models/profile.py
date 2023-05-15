from django.db import models
from authapp.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


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

    phone_number = models.PositiveBigIntegerField(
        blank=True,
        unique=True,
        validators=[
            MaxValueValidator(
                9999999999,
                message="Phone number must be entered "
                        "in the format '+71234567890'. 10 digits allowed."
            ),
            MinValueValidator(
                1000000000,
                message="Phone number must be entered "
                        "in the format '+71234567890'. 10 digits allowed."
            )
        ],
    )

    def __str__(self):
        return f'{self.fio} - {self.user.email}'

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
