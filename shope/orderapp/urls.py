from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

app_name = 'orderapp'

urlpatterns = [

    path('basket/', TemplateView.as_view(template_name="orderapp/basket.html")),
    path('checkout/', TemplateView.as_view(template_name="orderapp/checkout.html")),
    path('payment/', TemplateView.as_view(template_name="paymentapp/payment.html")),

]
