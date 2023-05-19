from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from coreapp.utils.products_comparison_list import ProductsComparisonList
from repositories import SpecificSelectRepository
from repositories.price_repository import PriceRepository


class ProductComparisonView(View):
    """
    Класс-view для сравнения товаров
    """
    _service = ProductsComparisonList()
    _price_repository = PriceRepository()
    _specific_repository = SpecificSelectRepository()
    template_name = "productsapp/comparison.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        request.session["comparison_list"] = [1, 2]
        # это тестовые продукты из фикстур
        products = self._service.get_comparison_list(request)
        for product in products:
            product_price = self._price_repository.get_avg_prices(
                product=product
            )
            product.product_price_avg = product_price
            specifics = self._specific_repository.get_specific_by_product(
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
        return render(request=request,
                      template_name=self.template_name,
                      context={
                          "products": products,
                          "number_of_products":
                              self._service.comparison_list_size(request)
                      })

    def post(self, request: HttpRequest):
        products = self._service.get_comparison_list(request)
        for product in products:
            product_price = self._price_repository.get_avg_prices(
                product=product
            )
            product.product_price_avg = product_price
            # Усредненная цена
            specifics = self._specific_repository.get_specific_by_product(
                product=product
            )
            # Получаем характеристики для продукта
            spec_name_list = list()
            # Список имён характеристик для данного продукта
            for specific in specifics:
                # Выделяем цветом характеристики
                current_name = specific.type_spec.name
                spec_name_list.append(current_name)

                if current_name in [
                    "Тип",
                    "Операционная система",
                    "Плотность пикселей"
                ]:
                    specific.is_comparis = True

            product.specifics = specifics
            product.spec_names = spec_name_list

        # Список общих имен характеристик

        common_names = list()

        if len(products) == 2:
            common_names = list(set(
                products[0].spec_names
            ).intersection(products[1].spec_names))
        elif len(products) == 3:
            common_names = list(set(
                products[0].spec_names
            ).intersection(products[1].spec_names).intersection(
                products[2].spec_names
            ))

        # Список общих характеристик

        common_spec = [
            specific
            for product in products
            for specific in product.specifics
            if specific.type_spec.name in common_names
        ]

        # Словарь, key - имя характеристики, value -
        # список разных значений данной характеристики

        spec_dict = dict()
        for spec in common_spec:
            name = spec.type_spec.name
            if name in spec_dict.keys():
                if spec.description not in spec_dict[name]:
                    spec_dict[name].append(spec.description)
            else:
                spec_dict[name] = [spec.description]

        if "is_different" in request.POST:
            # Только различающиеся характеристики
            for product in products:
                new_specifics = list()
                for specific in product.specifics:
                    name = specific.type_spec.name
                    if name in spec_dict.keys() \
                            and specific.description in spec_dict[name]:
                        new_specifics.append(specific)
                        # Отсеиваем характеристики, которых нет в общем списке
                        # и у которых одинаковые характеристики
                product.specifics = new_specifics

        return render(request=request,
                      template_name=self.template_name,
                      context={
                          "products": products,
                          "number_of_products":
                              self._service.comparison_list_size(request)
                      })
