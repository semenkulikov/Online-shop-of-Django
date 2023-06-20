from django.views.generic import View
from django.shortcuts import HttpResponseRedirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from coreapp.utils.select_cart import SelectCart
from repositories.cart_repository import RepCartItem
from repositories import RepCart
from repositories import OrderUpdateRepository, OrderItemUpdateRepository
from coreapp.utils import ProductDiscounts
from django.conf import settings

rep_cart = RepCart()
rep_cartitem = RepCartItem()
rep_order = OrderUpdateRepository()
rep_orderitem = OrderItemUpdateRepository()


class AddOrderView(LoginRequiredMixin, View):
    """Класс-view для создания нового заказа"""

    def post(self, request):

        user = request.user
        cart = rep_cart.get_cart(user=user)
        count = SelectCart.cart_all_products_amount(cart=cart)
        cart_price = SelectCart.cart_total_amount(cart=cart)
        total_sum = rep_cart.get_total_amount(cart)
        discounted_sum = sum(ProductDiscounts.get_prices_discount_on_cart(
            cart_price, count, cart=cart))
        sellers = rep_cartitem.sellers_amount(cart.pk)

        delivery_price = settings.DELIVERY_PRICE
        # доставка бесплатная если все товары от одного продавца и
        # сумма заказа больше требуемой
        if discounted_sum > settings.FREE_DELIVERY_SUM and sellers == 1:
            delivery_price = 0

        order = rep_order.save(  # создание нового заказа
            user=request.user,
            delivery_price=delivery_price,
            total_price=total_sum + delivery_price,
            total_discounted_price=discounted_sum + delivery_price
        )

        # перенос позиций из корзины в заказ
        cart_items = SelectCart.cart_items_list(user=request.user)
        rep_orderitem.create_with_cartitems(
            order=order,
            cart_items=cart_items)
        rep_cartitem.delete(cart_items)  # очистка корзины

        return HttpResponseRedirect(reverse('orderapp:edit_order',
                                            kwargs={'order_pk': order.pk}))
