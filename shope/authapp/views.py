from authapp.models import User
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from authapp.forms import UserLoginForm, UserSignUpForm
from django.contrib.auth.views import LoginView, LogoutView
from coreapp.utils.verified_user import send_verif_link, generate_random_string


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
            if send_verif_link(user):
                # если ссылка создана и отправлено сообщение
                messages.success(request, 'Вы успешно зарегистрировались.'
                                          ' \nСсылка для активации '
                                          'аккаунта отправлена на email')
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
                return render(request, 'authapp/verified.html')
        except Exception:
            return HttpResponseRedirect("index.html")
    return render(request, 'authapp/verified.html')
