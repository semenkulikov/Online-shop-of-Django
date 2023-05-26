from django.urls import path
from django.views.generic import TemplateView
from orderapp.views import OrderListView, OrderDetailView

app_name = 'orderapp'

urlpatterns = [

    path('historyorder/', OrderListView.as_view(), name='history_order'),
    path('oneorder/<int:order_pk>/', OrderDetailView.as_view(), name='oneorder'),
    path('', TemplateView.as_view(template_name="orderapp/order.html")),
]
