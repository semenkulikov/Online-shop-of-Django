from typing import List, Dict

from django.db.models import QuerySet
from productsapp.models import Product, Discount

from repositories.product_select_repository import ProductSelectRepository


_product_repository = ProductSelectRepository()


class ProductDiscounts:
    """
    Сервис получения скидок на товары
    """

    @staticmethod
    def all_discounts(products_id: List[int]) -> \
            Dict[Product, QuerySet[Discount]]:
        """
        Получение всех скидок на указанный список товаров или на один товар.
        """
        discounts = _product_repository.get_all_discounts(products_id)
        return discounts

    def priority_discount(self):
        """
        Получение приоритетной скидки на указанный список товаров
        или на один товар
        """
        pass

    def discounted_price(self):
        """
        Рассчитать цену со скидкой на товар с дополнительным
        необязательным параметром 'Цена товара'
        """
        pass
