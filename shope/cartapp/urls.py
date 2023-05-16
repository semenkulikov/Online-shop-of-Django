from django.urls import path
from cartapp.views import AddProductCartView, RemoveProductCartView, \
    DeleteItemCartView, CartItemListView


app_name = 'cartapp'
urlpatterns = [
    path('',
         CartItemListView.as_view(), name='cart'),
    path('catalog/add/<int:product_id>/',
         AddProductCartView.as_view(), name='add_product'),
    path('catalog/remove/<int:product_id>/',
         RemoveProductCartView.as_view(), name='remove_product'),
    path('catalog/delete/<int:product_id>/',
         DeleteItemCartView.as_view(), name='delete_product'),

]