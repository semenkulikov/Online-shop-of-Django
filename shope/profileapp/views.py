from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from repositories import OrderRepository
from django.shortcuts import render


order_rep = OrderRepository()


class ProfileView(View, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        account = Profile.objects.get(user=self.request.user)
        order = order_rep.get_last_activ(user=self.request.user)
        context = {
            'account': account,
            'order': order,
        }
        return render(request, 'profileapp/account.html', context=context)
