from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from repositories import OrderRepository

order_rep = OrderRepository()


class OrderDetailView(LoginRequiredMixin, DetailView):
    """ Класс-view для детальной информации по заказу """

    template_name = 'orderapp/oneorder.html'

    def get_object(self, queryset=None):
        order = order_rep.get_order_by_id(self.kwargs['order_pk'])
        return order
