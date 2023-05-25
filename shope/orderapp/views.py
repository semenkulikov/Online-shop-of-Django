from django.views.generic import View
from profileapp.forms import ProfileForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class OrderView(LoginRequiredMixin, View):
    template_name = 'orderapp/order.html'
    login_url = reverse_lazy('authapp:login')

    def get(self, request):
        context = {
            'profile_form': ProfileForm(
                instance=self.request.user.profile),
        }
        return render(request, self.template_name, context)
