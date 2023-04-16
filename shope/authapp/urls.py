from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

app_name = 'authapp'

urlpatterns = [
    path('resetpassword/mail/', TemplateView.as_view(template_name=
                                       "authapp/email_to_change_password.html")),
    path('login/', TemplateView.as_view(template_name=
                                        "authapp/login.html")),
    path('resetpassword/newpassword/', TemplateView.as_view(template_name=
                                           "authapp/change_password.html")),
    path('registr/', TemplateView.as_view(template_name=
                                          "authapp/registr.html")),

]
