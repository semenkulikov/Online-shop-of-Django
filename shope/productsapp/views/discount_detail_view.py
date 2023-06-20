from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from repositories import DiscountRepository, PriceRepository

_discount_repo = DiscountRepository()
_price_repository = PriceRepository()


class DiscountSetDetailView(View):
    """
    Представление для отображения
    детальной страницы скидки на набор продуктов
    """

    def get(self, request: HttpRequest, elem_id: int) -> HttpResponse:
        set_discount = _discount_repo.get_set_discount_by_id(elem_id)
        total_price = 0
        for product in set_discount.products.all():
            product_price = _price_repository. \
                get_min_price_object(product=product)
            product.product_price_avg = product_price
            total_price += product_price.value
        context = {
            "set_discount": set_discount,
            "total_price": total_price,
        }
        return render(request=request,
                      template_name="productsapp/detailed_discount.html",
                      context=context)


class DiscountCartDetailView(View):
    """ Представление для отображения детальной страницы скидки на корзину """

    def get(self, request: HttpRequest, elem_id: int) -> HttpResponse:
        cart_discount = _discount_repo.get_cart_discount_by_id(elem_id)
        context = {
            "cart_discount": cart_discount,
        }
        return render(request=request,
                      template_name="productsapp/detailed_discount.html",
                      context=context)
