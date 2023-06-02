from django.shortcuts import HttpResponseRedirect, reverse, render
from django.views.generic import View
from paymentapp.forms import PaymentForm
from profileapp.forms import ProfileForm
from orderapp.forms import OrderForm
from coreapp.utils.payment import Payment
from repositories import OrderRepository
from repositories import OrderUpdateRepository
from repositories import PaymentUpdateRepository
from coreapp.enums import SUCCEDED_STATUS, PAID_STATUS

order_rep = OrderRepository()
order_upd_rep = OrderUpdateRepository()
payment_upd_rep = PaymentUpdateRepository()


class PaymentView(View):

    def post(self, request, *args, **kwargs):
        order = order_rep.get_order_by_id(self.kwargs['order_pk'])

        order_form = OrderForm(
            request.POST,
            instance=order)
        profile_form = ProfileForm(
            request.POST,
            instance=self.request.user.profile)
        payment_form = PaymentForm(
            request.POST)

        if all((order_form.is_valid(),
                profile_form.is_valid(),
                payment_form.is_valid())):

            order_form.save()
            profile_form.save()

            card = {  # создание объекта карты для проведения платежа
                'number':
                    payment_form.cleaned_data['card_number'],
                'cardholder':
                    payment_form.cleaned_data['card_holder'],
                'csc':
                    payment_form.cleaned_data['cvv'],
                'expiry_month':
                    payment_form.cleaned_data['expiry_date'].strftime('%m'),
                'expiry_year':
                    payment_form.cleaned_data['expiry_date'].strftime('%Y')
            }

            # обращение к платежному сервису
            response = Payment.create_payment(
                amount=str(payment_form.cleaned_data['total_sum']),
                order_number=order.pk,
                card=card)

            if response.status_code == 200:
                payment_object = response.json()

                # создание объекта платежа в локальной базе
                payment_upd_rep.save(
                    amount=payment_object['amount']['value'],
                    payment_id=payment_object['id'],
                    status=payment_object['status'],
                    user=request.user,
                    order=order)

                # обновление статуса заказа в случае успешного платежа
                if payment_object['status'] == SUCCEDED_STATUS:
                    order_upd_rep.save(instance=order,
                                       status=PAID_STATUS)

            return HttpResponseRedirect(reverse('orderapp:oneorder',
                                                kwargs={'order_pk': order.pk}))

        else:
            total_sum = sum([item.price for item in order.order_items.all()])
            context = {
                'profile_form': profile_form,
                'order_form': order_form,
                'payment_form': payment_form,
                'order': order,
                'total_sum': total_sum,
            }
            return render(request, 'orderapp/order.html', context=context)
