from django.contrib.auth.forms import AuthenticationForm, \
    UserCreationForm, UsernameField
from authapp.models import User
from django import forms


class UserLoginForm(AuthenticationForm):
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
        for name_field, field in self.fields.items():
            field.widget.attrs['class'] = 'user-input'
