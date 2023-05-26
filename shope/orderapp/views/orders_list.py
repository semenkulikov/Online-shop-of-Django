from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from repositories import OrderRepository

order_rep = OrderRepository()


class OrderListView(LoginRequiredMixin, ListView):
    """ Класс-view для заказов """

    template_name = 'orderapp/historyorder.html'
    queryset = order_rep.get_all()
    ordering = '-created_at'
