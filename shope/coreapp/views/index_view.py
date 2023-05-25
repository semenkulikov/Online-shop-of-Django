from django.views.generic import View
from django.shortcuts import render
from repositories import SliderRepository, BannerRepository

slider_rep = SliderRepository()
banner_rep = BannerRepository()


class IndexView(View):

    template_name = 'index.html'

    def get(self, request):

        sliders = slider_rep.get_all()
        banners = banner_rep.get_random_banners()

        context = {
            'sliders': sliders,
            'banners': banners
        }

        return render(request, self.template_name, context=context)
