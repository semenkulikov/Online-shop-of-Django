from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile


class ProfileDetailView(DetailView, LoginRequiredMixin):
    queryset = Profile.objects.all()
    template_name = 'profileapp/account.html'

    def get_object(self, queryset=None):
        return self.request.user.profile
