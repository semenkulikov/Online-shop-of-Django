from django.urls import path
from django.views.generic import TemplateView
from productsapp.views import ProductListView, AddReviewView, ProductComparisonView

app_name = 'productsapp'

urlpatterns = [
    path('cart/',
         TemplateView.as_view(template_name="productsapp/cart.html")),
    path('catalog/', ProductListView.as_view(), name="catalog"),
    path('catalog/<int:product_id>/',
         TemplateView.as_view(template_name="productsapp/product.html")),
    path('catalog/<int:product_id>/add_review/', AddReviewView.as_view(), name="product_detail"),
    path('comparison/', ProductComparisonView.as_view(), name="comparison"),
    path('sale/',
         TemplateView.as_view(template_name="productsapp/sale.html"))
]
