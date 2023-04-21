from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

app_name = 'authapp'

urlpatterns = [
    path('forgot-password/', TemplateView.as_view(template_name=
                                       "authapp/forgot_password.html")),
    path('login/', TemplateView.as_view(template_name=
                                        "authapp/login.html")),
    path('set-password/', TemplateView.as_view(template_name=
                                           "authapp/set_password.html")),
    path('signup/', TemplateView.as_view(template_name=
                                          "authapp/registr.html")),

]
