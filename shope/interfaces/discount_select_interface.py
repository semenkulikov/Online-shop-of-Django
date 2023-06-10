from abc import ABC, abstractmethod
from productsapp.models import Product, SetDiscount
from django.db.models import QuerySet


class DiscountInterface(ABC):
    """
    Интерфейс для работы со скидками
    """

    @abstractmethod
    def get_discount_by_product_or_category(self, product, category):
        """
        Метод получения скидки на товар
        """
        pass

    @abstractmethod
    def get_discount_by_set_products(self, set_product):
        """
        Метод получения скидки на набор товаров
        """
        pass

    @abstractmethod
    def get_discount_by_cart(self):
        """
        Метод получения скидки на корзину
        """

    @abstractmethod
    def get_set_discounts_for_product(
            self, product: Product) -> QuerySet[SetDiscount]:
        """
        Получить все скидки на наборы, в которых есть данный продукт
        """
        pass
