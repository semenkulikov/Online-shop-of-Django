from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from productsapp.views import ProductListView, ProductDetailView

app_name = 'productsapp'

urlpatterns = [
    path('cart/',
         TemplateView.as_view(template_name="productsapp/cart.html")),
    path('catalog/', ProductListView.as_view(), name="catalog"),
    path('catalog/<int:product_id>/', ProductDetailView.as_view(), name="product_detail"),
    path('comparison/',
         TemplateView.as_view(template_name="productsapp/comparison.html")),
    path('sale/',
         TemplateView.as_view(template_name="productsapp/sale.html"))
]
