from django.views.generic import View
from django.shortcuts import HttpResponseRedirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from coreapp.utils.select_cart import SelectCart
from repositories.cart_repository import RepCartItem
from repositories import OrderUpdateRepository, OrderItemUpdateRepository

rep_cartitem = RepCartItem()
rep_order = OrderUpdateRepository()
rep_orderitem = OrderItemUpdateRepository()


class AddOrderView(LoginRequiredMixin, View):
    """Класс-view для создания нового заказа"""

    def post(self, request):
        cart_items = SelectCart.cart_items_list(user=request.user)
        order = rep_order.save(  # создание нового заказа
            user=request.user)

        # перенос позиций из корзины в заказ
        rep_orderitem.create_with_cartitems(
            order=order,
            cart_items=cart_items)
        rep_cartitem.delete(cart_items)  # очистка корзины

        return HttpResponseRedirect(reverse('orderapp:edit_order',
                                            kwargs={'order_pk': order.pk}))
