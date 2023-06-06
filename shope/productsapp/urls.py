from django.urls import path
from django.views.generic import TemplateView
from productsapp.views import (
    ProductListView,
    AddReviewView,
    ProductComparisonView,
    ProductDetailView,
    AddToComparisonView,
    RemoveFromComparisonView
    export_product_to_xls
)

app_name = 'productsapp'

urlpatterns = [
    path('catalog/', ProductListView.as_view(), name="catalog"),
    path('catalog/<int:product_id>/', ProductDetailView.as_view(), name="product_detail"),
    path('catalog/<int:product_id>/add_review/', AddReviewView.as_view(), name="add_review"),
    path('catalog/<int:product_id>/add_to_comparison/', AddToComparisonView.as_view(), name="add_to_comparison"),
    path('catalog/export/', export_product_to_xls, name="export_product"),
    path('comparison/', ProductComparisonView.as_view(), name="comparison"),
    path('comparison/<int:product_id>', RemoveFromComparisonView.as_view(), name="remove_from_comp"),
    path('sale/',
         TemplateView.as_view(template_name="productsapp/sale.html"))
]
