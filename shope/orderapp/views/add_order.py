from django.views.generic import View
from profileapp.forms import ProfileForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect


class AddOrderView(LoginRequiredMixin, View):
    template_name = 'orderapp/order.html'
    login_url = reverse_lazy('authapp:login')

    def get(self, request):
        context = {
            'profile_form': ProfileForm(
                instance=self.request.user.profile),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        return HttpResponseRedirect(reverse('coreapp:index'))
