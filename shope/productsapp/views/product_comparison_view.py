from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from coreapp.utils.products_comparison_list import ProductsComparisonList
from repositories import SpecificSelectRepository
from repositories.price_repository import PriceRepository


_price_repository = PriceRepository()
_specific_repository = SpecificSelectRepository()


class ProductComparisonView(View):
    """
    Класс-view для сравнения товаров
    """
    template_name = "productsapp/comparison.html"
    _service = ProductsComparisonList()

    def get(self, request: HttpRequest) -> HttpResponse:
        products = self._service.get_comparison_list(request) or []
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

    def post(self, request: HttpRequest):
        products = self._service.get_comparison_list(request) or []
        for product in products:
            product_price = _price_repository. \
                get_min_price_object(product=product)
            product.product_price_avg = product_price
            # Усредненная цена
            specifics = _specific_repository.get_specific_by_product(
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

        names = [set(product.spec_names) for product in products]
        common_names = set()
        for name_set in names:
            if common_names:
                common_names &= name_set  # пересечение множеств
            else:
                common_names |= name_set  # объединение множеств

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
                # Обновленный список характеристик
                for specific in product.specifics:
                    name = specific.type_spec.name
                    if name in spec_dict.keys() \
                            and specific.description in spec_dict[name]:
                        new_specifics.append(specific)
                        # Отсеиваем характеристики, которых нет в общем списке
                        # и у которых одинаковые характеристики
                product.specifics = new_specifics

        common_category: set = {product.category for product in products}

        return render(request=request,
                      template_name=self.template_name,
                      context={
                          "products": products,
                          "number_of_products":
                              self._service.comparison_list_size(request),
                          "is_common_spec": True
                          if not common_spec or len(common_category) > 1
                          else False,
                      })
