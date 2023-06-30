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
from .tasks import send_verif_link
from coreapp.utils import AddToCart, generate_random_string
from repositories.cart_repository import RepCart
from django.utils.translation import gettext as _


class UserLoginView(LoginView):
    """
    Авторизация пользователя.
    """
    template_name = 'authapp/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        super().form_valid(form)
        session_products = self.request.session.get('products')
        if self.request.user.is_authenticated and session_products:
            # если в сессии есть продукты
            AddToCart.move_from_session(self.request.user, session_products)
            # добавление товаров в продукты
        return HttpResponseRedirect(self.get_success_url())


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
    rep_cart = RepCart()

    def get(self, request, *args, **kwargs):
        form = self.form_class(data=request.GET)
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('coreapp:index'))
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():  # форма прошла валидацию
            user = form.save(commit=False)
            user.is_active = False  # деактивация пользователя
            user.activation_key = generate_random_string()
            user.save()
            protocol = request.scheme
            domain = request.META['HTTP_HOST']
            session_products = request.session.get('products')
            if session_products:  # если в сессии есть продукты
                AddToCart.move_from_session(user, session_products)
            send_verif_link.delay(protocol, domain, user.email,
                                  user.activation_key,
                                  user.first_name, user.last_name)
            # ссылка создана и отправлено сообщение
            messages.success(request, _(
                'You have successfully registered. '
                '\nThe account activation link has been emailed to you.'
                '\n You must confirm your account within 72 hours.'))
            return HttpResponseRedirect(reverse('authapp:login'))
        else:  # при наличии ошибок в форме
            messages.set_level(request, messages.ERROR)
            messages.error(request, *list(form.errors.values()))
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
        except Exception:
            messages.error(request, _('An error has occurred. '
                                      'The activation period has expired'
                                      '\nTry registering again.'))
    return HttpResponseRedirect(reverse('coreapp:index'))


class UserPassResetView(PasswordResetView):
    """
    Класс для отработки отправки токена для смены пароля на
    электронную почту.
    """
    form_class = UserResetPasswordForm
    template_name = "authapp/forgot_password.html"
    from_email = settings.EMAIL_HOST_USER
    html_email_template_name = "authapp/email/reset_confirm.html"
    email_template_name = 'authapp/email/reset_confirm.html'
    success_url = reverse_lazy('authapp:login')

    def form_valid(self, form):
        messages.success(self.request,
                         _('Link to change your password '
                           'was sent to your email address')
                         )
        return super().form_valid(form)


class UserPassChangeView(PasswordResetConfirmView):
    """
    Класс для смены пароля
    """
    form_class = UserSetPasswordForm
    template_name = "authapp/set_password.html"
    success_url = reverse_lazy('authapp:login')

    def form_valid(self, form):
        messages.success(self.request,
                         _('Your password has been successfully changed')
                         )
        return super().form_valid(form)
