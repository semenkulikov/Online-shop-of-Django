from django.views.generic import View
from django.shortcuts import render
from repositories import (
    SliderRepository,
    BannerRepository,
    ProductSelectRepository,
)

slider_rep = SliderRepository()
banner_rep = BannerRepository()
product_rep = ProductSelectRepository()


class IndexView(View):

    template_name = 'index.html'

    def get(self, request):

        sliders = slider_rep.get_all()
        banners = banner_rep.get_random_banners()
        products = product_rep.get_all_products_with_main_image()

        popular = product_rep.sort_by_popular(products=products, reverse=True)
        popular = product_rep.get_product_prices(popular)

        context = {
            'sliders': sliders,
            'banners': banners,
            'populars': popular
        }

        return render(request, self.template_name, context=context)
