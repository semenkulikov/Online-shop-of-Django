from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from profileapp.forms import ProfileForm
from orderapp.forms import OrderForm
from paymentapp.forms import PaymentForm
from coreapp.utils.select_cart import SelectCart
from repositories.price_repository import PriceRepository
from repositories.cart_repository import RepCartItem
from repositories import OrderUpdateRepository
from repositories import OrderItemUpdateRepository
from coreapp.enums import NOT_PAID_STATUS

rep_price = PriceRepository()
rep_cartitem = RepCartItem()
rep_order = OrderUpdateRepository()
rep_orderitem = OrderItemUpdateRepository()


class AddOrderView(LoginRequiredMixin, View):
    template_name = 'orderapp/order.html'

    def post(self, request):
        cart_items = SelectCart.cart_items_list(user=request.user)
        order = rep_order.save(  # создание нового заказа
            user=request.user,
            status=NOT_PAID_STATUS)

        # перенос позиций из корзины в заказ
        order_items = rep_orderitem.create_with_cartitems(
            order=order,
            cart_items=cart_items)
        total_sum = sum([item.price for item in order_items])
        rep_cartitem.delete(cart_items)  # очистка корзины

        profile_form = ProfileForm(
            instance=self.request.user.profile)

        payment_form = PaymentForm()
        payment_form.fields['total_sum'].initial = total_sum

        context = {
            'profile_form': profile_form,
            'order_form': OrderForm(),
            'payment_form': payment_form,
            'order': order,
            'total_sum': total_sum,
        }
        return render(request, self.template_name, context)
