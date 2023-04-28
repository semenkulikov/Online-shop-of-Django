from django.apps import AppConfig
# flake8: noqa


class AuthappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapp'
    verbose_name = 'Пользователи'
