from django.urls import path
from .views import IndexView, clear_cache

app_name = 'coreapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('clear_cache/', clear_cache, name="clear_cache"),
]
