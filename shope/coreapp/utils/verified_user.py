import secrets
import string
from django.conf import settings
from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import get_template


def send_verif_link(user, protocol, domain):
    """
    Метод создания и отправки сообщения на e-mail
    :return: send_mail
    :rtype: bool
    """
    site_name = f'{protocol}://{domain}'
    verif_link = site_name + reverse('authapp:verified',
                                     kwargs={'email': user.email,
                                             'key': user.activation_key
                                             }
                                     )  # ссылка для активации
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'link': verif_link,
    }
    message = get_template('authapp/email/email_confirm.html').render(context)
    subject = f'Email confirmation on {site_name}'  # тема
    msg = EmailMessage(
        subject, message, to=[user.email], from_email=settings.EMAIL_HOST_USER
    )
    msg.content_subtype = 'html'
    try:
        msg.send()  # отправка сообщения на user.email
    except Exception as ex:
        print(ex)
        return False
    return True


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

# def send_verif_link(user):
#     """
#     Метод создания и отправки сообщения на e-mail
#     :return: send_mail
#     :rtype: bool
#     """
#     verif_link = reverse('authapp:verified',
#                          kwargs={'email': user.email,
#                                  'key': user.activation_key
#                                  }
#                          )  # ссылка для активации
#     subject = 'Активация аккаунта'  # тема
#     message = f'Для подтверждения электронной почты' \
#               f' {user.email} на портале \n ' \
#               f'{settings.DOMAIN_NAME} пройдите по ссылке \n' \
#               f'{settings.DOMAIN_NAME}{verif_link}'
#     # сообщение
#     return send_mail(subject, message,
#                      settings.EMAIL_HOST_USER,
#                      [user.email])  # отправка email
