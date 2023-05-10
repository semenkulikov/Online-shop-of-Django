from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from repositories import OrderRepository


order_rep = OrderRepository()


class ProfileDetailView(DetailView, LoginRequiredMixin):
    queryset = Profile
    template_name = 'profileapp/account.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = order_rep.get_last_activ(user=self.request.user)
        return context
