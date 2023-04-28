import secrets
import string
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


def send_verif_link(user):
    """
    Метод создания и отправки сообщения на e-mail
    :return: send_mail
    :rtype: bool
    """
    verif_link = reverse('authapp:verified',
                         kwargs={'email': user.email,
                                 'key': user.activation_key
                                 }
                         )  # ссылка для активации
    subject = 'Активация аккаунта'  # тема
    message = f'Для подтверждения электронной почты' \
              f' {user.email} на портале \n ' \
              f'Megano Shop пройдите по ссылке \n' \
              f'{settings.DOMAIN_NAME}{verif_link}'
    # сообщение
    return send_mail(subject, message,
                     settings.EMAIL_HOST_USER,
                     [user.email])  # отправка email


def generate_random_string():
    """
    Метод, который генерирует случайный ключ активации из 13 символов
    return: rand_string
    rtype: string
    """
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(secrets.choice(
        letters_and_digits) for i in range(13))
    return rand_string
