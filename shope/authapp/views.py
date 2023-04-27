import secrets
import string
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from authapp.forms import UserLoginForm, UserSignUpForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from authapp.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login


class UserLoginView(LoginView):
    """
    Авторизация пользователя.
    """
    template_name = 'authapp/login.html'
    form_class = UserLoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        return render(request, self.template_name, {'form': self.form_class})


class UserLogoutView(LogoutView):
    next_page = '../'


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


class UserSignUpView(CreateView):
    """
    Регистрация пользователя
    """
    model = User
    template_name = 'authapp/registr.html'
    form_class = UserSignUpForm
    success_url = reverse_lazy('authapp:login')

    def get(self, request, *args, **kwargs):
        form = self.form_class(data=request.GET)
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():  # форма прошла валидацию
            user = form.save(commit=False)
            user.is_active = False  # деактивация пользователя
            user.activation_key = generate_random_string()
            user.save()
            if self.send_verif_link(user):
                # если ссылка создана и отправлено сообщение
                messages.success(request, 'Вы успешно зарегистрировались.'
                                          ' \nСсылка для активации '
                                          'аккаунта отправлена на email')
                return HttpResponseRedirect(reverse('authapp:login'))
        else:
            messages.error(request, form.errors)  # при наличии ошибок в форме
        return render(request, self.template_name, {'form': form})

    def send_verif_link(self, user):
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
        subject = 'Активация аккаунта'
        message = f'Для подтверждения электронной почты' \
                  f' {user.email} на портале \n ' \
                  f'Megano Shop пройдите по ссылке \n' \
                  f'http://127.0.0.1:8000{verif_link}'
        # позже добавлю {settings.DOMAIN_NAME}
        # вместо "Megano Shop"
        return send_mail(subject, message,
                         settings.EMAIL_HOST_USER,
                         [user.email])  # отправка mail


def verify_user(request, *args, **kwargs):
    """
    Активация учетной записи
    :return: Response
    :rtype: HttpResponse
    """
    if request.method == 'GET':
        try:
            email = kwargs.get('email')  # мейл из запроса
            activate_key = kwargs.get('key')  # ключ из запроса
            user = User.objects.get(email=email)
            print(user.is_activation_key_expires)
            if user and user.activation_key == activate_key and \
                    not user.is_activation_key_expires:
                # если еще не прошло 72 часа
                # с момента регистрации и ключи одинаковые
                user.activation_key = ""
                user.is_active = True
                user.activation_key_expires = None
                user.save()
                login(request, user)  # вход в учетную запись
                return render(request, 'authapp/verified.html')
        except Exception:
            return HttpResponseRedirect("index.html")
    return render(request, 'authapp/verified.html')
