from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('profile/', TemplateView.as_view(template_name="profileapp/profile.html")),
    path('account/', TemplateView.as_view(template_name="profileapp/account.html")),
    path('profileAvatar/', TemplateView.as_view(template_name="profileapp/profileAvatar.html"))
]
