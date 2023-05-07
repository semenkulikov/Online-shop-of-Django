from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import ProfileView

app_name = 'profileapp'

urlpatterns = [
    path('account/', ProfileView.as_view(), name='account'),
    path('profile/', TemplateView.as_view(
        template_name='profileapp/profile.html'), name='profile_update'),
]
