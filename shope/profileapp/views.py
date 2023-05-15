from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Profile
from repositories import OrderRepository
from .forms import ProfileForm, UserForm, UserPasswordSetForm
from django.shortcuts import render, redirect

order_rep = OrderRepository()


class ProfileDetailView(DetailView, LoginRequiredMixin):
    """
    View класс для отображения информации об аккаунте
    """
    queryset = Profile
    template_name = 'profileapp/account.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = order_rep.get_last_activ(user=self.request.user)
        return context


class ProfileUpdateView(View, LoginRequiredMixin):
    """
    View-класс для обновления информации о пользователе
    """
    template_name = 'profileapp/profile.html'
    success_message = 'Profile is updated successfully'

    def get(self, request):
        context = {
            'user_form': UserForm(instance=self.request.user),
            'profile_form': ProfileForm(instance=self.request.user.profile),
            'password_form': UserPasswordSetForm(user=self.request.user)
        }

        return render(request, self.template_name, context)

    def post(self, request):
        profile_form = ProfileForm(request.POST,
                                   request.FILES,
                                   instance=self.request.user.profile)

        user_form = UserForm(request.POST,
                             instance=self.request.user)

        password_form = UserPasswordSetForm(data=request.POST,
                                            user=request.user)

        if all([profile_form.is_valid(),
                user_form.is_valid(),
                password_form.is_valid()]):

            profile_form.save()
            user_form.save()
            password_form.save()
            messages.success(request, self.success_message)
            return redirect(self.request.path)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'password_form': password_form
        }

        return render(request, self.template_name, context=context)
