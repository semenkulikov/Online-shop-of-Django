from django.shortcuts import HttpResponseRedirect, reverse
from django.views.generic import View
from paymentapp.forms import PaymentForm
from profileapp.forms import ProfileForm
from orderapp.forms import OrderForm
from coreapp.utils.payment import Payment as PayNow
from repositories import OrderRepository
from paymentapp.models import Payment

order_rep = OrderRepository()


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
            card = {
                'number': payment_form.cleaned_data['card_number'],
                'cardholder': payment_form.cleaned_data['card_holder'],
                'csc': payment_form.cleaned_data['cvv'],
                'expiry_month':
                    payment_form.cleaned_data['expiry_date'].strftime('%m'),
                'expiry_year':
                    payment_form.cleaned_data['expiry_date'].strftime('%Y')
            }
            print(card)
            order_form.save()
            profile_form.save()

            response = PayNow.create_payment(
                amount=str(payment_form.cleaned_data['total_sum']),
                order_number=order.pk,
                card=card)

            if response.status_code == 200:
                payment_object = response.json()

                payment = Payment(
                    amount=payment_object['amount']['value'],
                    payment_id=payment_object['id'],
                    status=payment_object['status'],
                    user=request.user,
                    order=order)

                payment.save()

            print(response.status_code)
            print(response.text)

        return HttpResponseRedirect(reverse('orderapp:oneorder',
                                            kwargs={'order_pk': order.pk}))
