from typing import List, Dict

from django.db.models import QuerySet
from productsapp.models import Product, Discount

from repositories.product_select_repository import ProductSelectRepository


class ProductDiscounts:
    """
    Сервис получения скидок на товары
    """
    product_repository = ProductSelectRepository()

    def all_discounts(self, products_id: List[int]) -> \
            Dict[Product, QuerySet[Discount]]:
        """
        Получение всех скидок на указанный список товаров или на один товар.
        """
        discounts = self.product_repository.get_all_discounts(products_id)
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
