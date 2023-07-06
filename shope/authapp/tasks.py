from celery import shared_task
from django.conf import settings
from django.urls import reverse
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _


@shared_task
def send_verif_link(protocol, domain, email,
                    activation_key, first_name, last_name):
    """
    Метод создания и отправки сообщения на e-mail
    для подтверждения регистрации
    :return: send_mail
    :rtype: bool
    """
    site_name = f'{protocol}://{domain}'
    verif_link = site_name + reverse('authapp:verified',
                                     kwargs={'email': email,
                                             'key': activation_key
                                             }
                                     )  # ссылка для активации
    context = {
        'first_name': first_name, 'last_name': last_name, 'link': verif_link,
    }
    message = get_template('authapp/email/email_confirm.html').render(context)
    subject = _('Email confirmation on') + f' {site_name}'  # тема
    msg = EmailMessage(
        subject, message, to=[email], from_email=settings.EMAIL_HOST_USER
    )
    msg.content_subtype = 'html'
    try:
        msg.send()  # отправка сообщения на user.email
    except Exception as ex:
        print(ex)
        return False
    return True


@shared_task
def send_link_for_password(subject,
                           body,
                           from_email,
                           to_email,
                           html_email):
    """
    Метод для создания и отправки сообщения на e-mail адрес
    для смены пароля.
    :return: None
    """
    # Email subject *must not* contain newlines
    email_message = EmailMultiAlternatives(subject,
                                           body,
                                           from_email,
                                           [to_email])
    email_message.attach_alternative(html_email, "text/html")
    email_message.send()  # отправка сообщения
