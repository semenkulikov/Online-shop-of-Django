from django.urls import path
from cartapp.views import (
    AddToCartView,
    RemoveFromCartView,
    DeleteItemCartView,
    CartItemListView,
    ChangeQuantityCartView,
    AddToCartAjaxView,
    RemoveFromCartAjaxView,
    DeleteCartItemAjaxView,
    ChangeQuantityCartAjaxView
)

app_name = 'cartapp'
urlpatterns = [
    path('',
         CartItemListView.as_view(), name='cart'),
    path('catalog/add/<int:product_id>/<int:seller_id>/<int:count>/',
         AddToCartView.as_view(), name='add_product'),
    path('catalog/add/<int:product_id>/<int:seller_id>/',
         AddToCartView.as_view(), name='add_product'),
    path('catalog/remove/<int:product_id>/<int:seller_id>/',
         RemoveFromCartView.as_view(), name='remove_product'),
    path('catalog/delete/<int:product_id>/<int:seller_id>/',
         DeleteItemCartView.as_view(), name='delete_product'),
    path('catalog/change-count/<int:product_id>/<int:seller_id>/<int:count>/',
         ChangeQuantityCartView.as_view(), name='change_count'),
    path('catalog/ajax_add/<int:product_id>/<int:seller_id>/',
         AddToCartAjaxView.as_view(), name='ajax_add_product'),
    path('catalog/ajax_remove/<int:product_id>/<int:seller_id>/',
         RemoveFromCartAjaxView.as_view(), name='ajax_remove_product'),
    path('catalog/ajax_delete/<int:product_id>/<int:seller_id>/<int:full>/',
         DeleteCartItemAjaxView.as_view(), name='ajax_delete_product'),
    path('catalog/ajax_change-count/<int:product_id>/<int:seller_id>/<int:count>/',
         ChangeQuantityCartAjaxView.as_view(), name='ajax_change_count'),
]
