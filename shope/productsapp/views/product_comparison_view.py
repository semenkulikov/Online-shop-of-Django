from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from coreapp.utils.products_comparison_list import ProductsComparisonList


class ProductComparisonView(View):
    """
    Класс-view для сравнения товаров
    """
    _service = ProductsComparisonList()

    def get(self, request: HttpRequest) -> HttpResponse:
        request.session["comparison_list"] = [1, 2]
        # это тестовые продукты из фикстур
        products = self._service.get_comparison_list(request)
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
