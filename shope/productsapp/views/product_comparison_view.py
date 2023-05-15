from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from coreapp.utils.products_comparison_list import ProductsComparisonList
from repositories.price_repository import PriceRepository


class ProductComparisonView(View):
    """
    Класс-view для сравнения товаров
    """
    _service = ProductsComparisonList()
    _price_repository = PriceRepository()

    def get(self, request: HttpRequest) -> HttpResponse:
        request.session["comparison_list"] = [1, 2]
        # это тестовые продукты из фикстур
        products = self._service.get_comparison_list(request)
        for product in products:
            product_price = self._price_repository.get_avg_prices(
                product=product
            )
            product.product_price_avg = product_price

        return render(request=request,
                      template_name="productsapp/comparison.html",
                      context={
                          "products": products,
                          "number_of_products":
                              self._service.comparison_list_size(request)
                      })

    def post(self, request: HttpRequest):
        products = self._service.get_comparison_list(request)
        is_different = request.POST["is_different"]
        # Только различающиеся характеристики
        if is_different:
            pass
        return render(request=request,
                      template_name="productsapp/comparison.html",
                      context={
                          "products": products,
                          "number_of_products":
                              self._service.comparison_list_size(request)
                      })
