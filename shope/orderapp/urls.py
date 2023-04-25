from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

app_name = 'orderapp'

urlpatterns = [

    path('historyorder/', TemplateView.as_view(template_name="orderapp/historyorder.html")),
    path('oneorder/', TemplateView.as_view(template_name="orderapp/oneorder.html")),
    path('', TemplateView.as_view(template_name="orderapp/order.html")),
]
