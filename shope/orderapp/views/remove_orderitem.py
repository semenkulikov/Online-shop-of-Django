from django.views.generic import View
from django.shortcuts import HttpResponseRedirect, reverse
from repositories import OrderItemUpdateRepository, OrderRepository
from django.contrib.auth.mixins import LoginRequiredMixin

rep_orderitem = OrderItemUpdateRepository()
rep_order = OrderRepository()


class RemoveOrderItemView(LoginRequiredMixin, View):
    """Класс-представление для удаление позиции из заказа"""

    def get(self, request, order_pk: int, orderitem_pk: int):

        order = rep_order.get_order_by_id(order_pk)
        # В заказе должна быть хотя бы одна позиция
        if order.order_items.all().count() > 1:
            rep_orderitem.delete(orderitem_pk)

        return HttpResponseRedirect(reverse(
            'orderapp:edit_order', kwargs={'order_pk': order_pk}))
