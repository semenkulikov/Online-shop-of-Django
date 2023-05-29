from django.views.generic import View
from profileapp.forms import ProfileForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from orderapp.forms import OrderForm
from coreapp.utils.select_cart import SelectCart
from orderapp.models import Order, OrderItem
from repositories.price_repository import PriceRepository
from repositories.cart_repository import RepCartItem

rep_price = PriceRepository()
rep_cartitem = RepCartItem()


class AddOrderView(LoginRequiredMixin, View):
    template_name = 'orderapp/order.html'
    login_url = reverse_lazy('authapp:login')

    def get(self, request):
        cart_items = SelectCart.cart_items_list(user=request.user)
        print(cart_items)
        order = Order(user=request.user, status='not paid')
        order.save()
        for item in cart_items:
            order_item = OrderItem(
                order=order,
                product=item.product,
                seller=item.seller,
                count=item.quantity,
                price=rep_price.get_price(
                    item.product, item.seller) * item.quantity)
            order_item.save()

        rep_cartitem.delete(cart_items)
        profile_form = ProfileForm(instance=self.request.user.profile)
        for name, field in profile_form.fields.items():
            field.widget.attrs['id'] = name

        context = {
            'profile_form': profile_form,
            'order_form': OrderForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        return HttpResponseRedirect(reverse('coreapp:index'))
