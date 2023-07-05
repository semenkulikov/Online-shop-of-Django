from typing import List, Dict, Tuple
from django.db.models import QuerySet
from productsapp.models import Product, Specific


def get_general_characteristics(products: QuerySet[Product])\
        -> Tuple[Dict[str, list], List[Specific]]:
    """
    Функция для получения общих характеристик и их значений.
    :param products: кверисет продуктов
    :return: tuple(dict(str, list), list)
    """
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

    return spec_dict, common_spec
