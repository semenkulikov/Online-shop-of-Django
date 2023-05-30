from django.views.generic import View
from profileapp.forms import ProfileForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from orderapp.forms import OrderForm
from coreapp.utils.select_cart import SelectCart
from repositories.price_repository import PriceRepository
from repositories.cart_repository import RepCartItem
from repositories.order_update_repository import OrderUpdateRepository
from repositories.orderitem_update_repository import OrderItemUpdateRepository
from paymentapp.forms import PaymentForm

rep_price = PriceRepository()
rep_cartitem = RepCartItem()
rep_order = OrderUpdateRepository()
rep_orderitem = OrderItemUpdateRepository()


class AddOrderView(LoginRequiredMixin, View):
    template_name = 'orderapp/order.html'
    login_url = reverse_lazy('authapp:login')

    def get(self, request):
        cart_items = SelectCart.cart_items_list(user=request.user)
        order = rep_order.create(user=request.user)

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

    def post(self, request):
        return HttpResponseRedirect(reverse('coreapp:index'))
