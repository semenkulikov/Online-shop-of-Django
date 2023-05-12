from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import ProfileDetailView, ProfileUpdateView

app_name = 'profileapp'

urlpatterns = [
    path('account/', ProfileDetailView.as_view(), name='account'),
    path('profile/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile2/', TemplateView.as_view(template_name='profileapp/profileAvatar.html')),
]
