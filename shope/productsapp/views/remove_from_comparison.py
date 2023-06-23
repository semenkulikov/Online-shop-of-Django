from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from coreapp.utils.products_comparison_list import ProductsComparisonList
from repositories import SpecificSelectRepository
from repositories.price_repository import PriceRepository


_price_repository = PriceRepository()
_specific_repository = SpecificSelectRepository()


class RemoveFromComparisonView(View):
    """
    Класс-view для сравнения товаров
    """
    template_name = "productsapp/comparison.html"
    _service = ProductsComparisonList()

    def get(self, request: HttpRequest) -> HttpResponse:
        products = self._service.get_comparison_list(request)
        for product in products:
            product_price = _price_repository. \
                get_min_price_object(product=product)
            product.product_price_avg = product_price
            specifics = _specific_repository.get_specific_by_product(
                product=product
            )
            for specific in specifics:
                if specific.type_spec.name in [
                    "Тип",
                    "Операционная система",
                    "Плотность пикселей"
                ]:
                    specific.is_comparis = True
            product.specifics = specifics

        # Множество общих категорий, если разные
        # категории у разных продуктов - не сравниваем
        common_category: set = {product.category for product in products}

        return render(request=request,
                      template_name=self.template_name,
                      context={
                          "products": products,
                          "number_of_products":
                              self._service.comparison_list_size(request),
                          "is_common_spec": True
                          if len(common_category) > 1
                          else False,
                      })

    def post(self, request: HttpRequest, product_id: int):
        self._service.remove_from_comparison(request, product_id)
        return HttpResponseRedirect(reverse("productsapp:comparison"))
