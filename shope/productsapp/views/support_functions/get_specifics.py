from django.db.models import QuerySet

from productsapp.models import Product
from repositories import PriceRepository, SpecificSelectRepository

_price_repository = PriceRepository()
_specific_repository = SpecificSelectRepository()


def get_specifics(products: QuerySet[Product]) -> QuerySet[Product]:
    for product in products:
        product_price = _price_repository. \
            get_min_price_object(product=product)
        product.price = product_price.value
        # Цена
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

    return products
