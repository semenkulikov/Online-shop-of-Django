from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

app_name = 'productsapp'

urlpatterns = [
    path('cart/',
         TemplateView.as_view(template_name="productsapp/cart.html")),
    path('catalog/',
         TemplateView.as_view(template_name="productsapp/catalog.html")),
    path('comparison/',
         TemplateView.as_view(template_name="productsapp/comparison.html")),
    path('product/',
         TemplateView.as_view(template_name="productsapp/product.html")),
    path('sale/',
         TemplateView.as_view(template_name="productsapp/sale.html"))
]
