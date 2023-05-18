from django import forms
from authapp.models import User
from django.contrib.auth.forms import AuthenticationForm, \
    UserCreationForm, UsernameField, SetPasswordForm, \
    PasswordResetForm


class UserLoginForm(AuthenticationForm):
    """
    Форма для авторизации пользователя
    """
    username = UsernameField(
        widget=forms.TextInput(
            attrs={"autofocus": True,
                   "placeholder": "e-mail"
                   })
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.
        PasswordInput(
            attrs={"autocomplete": "current-password",
                   "placeholder": "********"
                   })
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class UserSignUpForm(UserCreationForm):
    """
    Форма для регистрации пользователя
    """
    class Meta:
        model = User
        fields = ('email', 'first_name',
                  'middle_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password2'].widget. \
            attrs['placeholder'] = 'Подтверждение пароля'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        self.fields['middle_name'].widget.attrs['placeholder'] = 'Отчество'
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True
        for name_field, field in self.fields.items():
            field.widget.attrs['class'] = 'user-input'


class UserResetPasswordForm(PasswordResetForm):
    """
    Форма для ввода email
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'


class UserSetPasswordForm(SetPasswordForm):
    """
    Форма для ввода нового пароля
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['new_password2'].widget. \
            attrs['placeholder'] = 'Подтверждение пароля'
