from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

app_name = 'authapp'

urlpatterns = [
    path('mail/', TemplateView.as_view(template_name=
                                       "authapp/mail.html")),
    path('login/', TemplateView.as_view(template_name=
                                        "authapp/login.html")),
    path('password/', TemplateView.as_view(template_name=
                                           "authapp/password.html")),
    path('registr/', TemplateView.as_view(template_name=
                                          "authapp/registr.html")),

]
