from django.urls import path
from orderapp.views import OrderListView, OrderDetailView, AddOrderView


app_name = 'orderapp'

urlpatterns = [

    path('historyorder/', OrderListView.as_view(), name='history_order'),
    path('oneorder/<int:order_pk>/', OrderDetailView.as_view(), name='oneorder'),
    path('', AddOrderView.as_view(), name='add_order'),
]
