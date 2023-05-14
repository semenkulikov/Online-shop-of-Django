from authapp.models import User
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetView, \
    PasswordResetConfirmView
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, \
    reverse
from authapp.forms import UserLoginForm, UserSignUpForm, \
    UserResetPasswordForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, LogoutView
from coreapp.utils.verified_user import send_verif_link, generate_random_string
from coreapp.utils.add_to_cart import AddToCart
from repositories.cart_repository import RepCart


class UserLoginView(LoginView):
    """
    Авторизация пользователя.
    """
    template_name = 'authapp/login.html'
    form_class = UserLoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return render(request, self.template_name, {'form': self.form_class})

    def form_valid(self, form):
        super().form_valid(form)
        if self.request.user.is_authenticated and self.request. \
                session.get('products'):
            # если в сессии есть продукты
            AddToCart().move_from_session(self.request, self.request.user)
            # добавление товаров в продукты
        return HttpResponseRedirect(reverse('index'))


class UserLogoutView(LogoutView):
    next_page = '/'


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
            return HttpResponseRedirect(reverse('index'))
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():  # форма прошла валидацию
            user = form.save(commit=False)
            user.is_active = False  # деактивация пользователя
            user.activation_key = generate_random_string()
            user.save()
            RepCart().save(user=user)
            if request.session['products']:  # если в сессии есть продукты
                AddToCart().move_from_session(request, user)
            if send_verif_link(user):
                # если ссылка создана и отправлено сообщение
                messages.success(request, 'Вы успешно зарегистрировались.'
                                          ' \nСсылка для активации '
                                          'аккаунта отправлена на email.\n'
                                          'В течение 72 часов Вам необходимо '
                                          'подтвердить свою учетную запись.')
                return HttpResponseRedirect(reverse('authapp:login'))
        else:
            messages.error(request, form.errors)  # при наличии ошибок в форме
        return render(request, self.template_name, {'form': form})


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
            if user and user.activation_key == activate_key and \
                    not user.is_activation_key_expires:
                # если еще не прошло 72 часа
                # с момента регистрации и ключи одинаковые
                user.activation_key = ""
                user.is_active = True  # активация пользователя
                user.activation_key_expires = None
                user.save()
                login(request, user)  # вход в учетную запись
                messages.set_level(request, messages.SUCCESS)
        except Exception:
            messages.error(request, 'Произошла ошибка. Истёк срок активации\n'
                                    'Попробуйте регистрацию заново.')
    return HttpResponseRedirect(reverse('index'))


class UserPassResetView(PasswordResetView):
    """
    Класс для отработки отправки токена для смены пароля на
    электронную почту.
    """
    form_class = UserResetPasswordForm
    template_name = "authapp/forgot_password.html"
    from_email = settings.EMAIL_HOST_USER
    html_email_template_name = "authapp/reset_confim.html"
    success_url = reverse_lazy('index')
    subject_template_name = "authapp/password_reset_subject.html"


class UserPassChangeView(PasswordResetConfirmView):
    """
    Класс для смены пароля
    """
    form_class = UserSetPasswordForm
    template_name = "authapp/set_password.html"
    success_url = reverse_lazy('index')
