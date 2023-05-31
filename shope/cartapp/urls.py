from django.urls import path
from cartapp.views import AddProductCartView, RemoveProductCartView, \
    DeleteItemCartView, CartItemListView, ChangeQuantityCartView, AjaxAddProductView

app_name = 'cartapp'
urlpatterns = [
    path('',
         CartItemListView.as_view(), name='cart'),
    path('catalog/add/<int:product_id>/<int:seller_id>/<int:count>/',
         AddProductCartView.as_view(), name='add_product'),
    path('catalog/add/<int:product_id>/<int:seller_id>/',
         AddProductCartView.as_view(), name='add_product'),
    path('catalog/remove/<int:product_id>/<int:seller_id>/',
         RemoveProductCartView.as_view(), name='remove_product'),
    path('catalog/delete/<int:product_id>/<int:seller_id>/',
         DeleteItemCartView.as_view(), name='delete_product'),
    path('catalog/change-count/<int:product_id>/<int:seller_id>/<int:count>/',
         ChangeQuantityCartView.as_view(), name='change_count'),
    path('catalog/ajax_add/<int:product_id>/<int:seller_id>/<int:count>/',
         AjaxAddProductView.as_view(), name='ajax_add_product'),

]
