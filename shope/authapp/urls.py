from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from authapp.views import UserLoginView, UserLogoutView, UserSignUpView, verify_user

app_name = 'authapp'

urlpatterns = [
    path('forgot-password/', TemplateView.as_view(template_name="authapp/forgot_password.html"),
         name='forgot_pass'),
    path('login/', UserLoginView.as_view(),
         name='login'),
    path('set-password/', TemplateView.as_view(template_name="authapp/set_password.html"),
         name='set_pass'),
    path('signup/', UserSignUpView.as_view(),
         name='signup'),
    path('logout/', UserLogoutView.as_view(),
         name='logout'),
    path('verified/<str:email>/<str:key>/', verify_user,
         name='verified'
         ),
]
