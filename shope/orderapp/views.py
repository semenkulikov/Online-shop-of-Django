from django.views.generic import View
from profileapp.forms import ProfileForm, UserForm, UserPasswordSetForm
from django.shortcuts import render


class OrderView(View):
    template_name = 'orderapp/order.html'

    def get(self, request):
        if request.user.is_authenticated:
            context = {
                'user_form': UserForm(
                    instance=self.request.user),
                'profile_form': ProfileForm(
                    instance=self.request.user.profile),
                'password_form': UserPasswordSetForm(
                    user=self.request.user)
            }
        else:
            context = {
                'user_form': UserForm(),
                'profile_form': ProfileForm(),
                'password_form': UserPasswordSetForm(
                    user=self.request.user)
            }
        return render(request, self.template_name, context)
