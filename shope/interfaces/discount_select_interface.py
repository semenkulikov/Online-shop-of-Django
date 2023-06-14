from abc import ABC, abstractmethod
from productsapp.models import Product, Category, \
    SetDiscount, ProductDiscount, CartDiscount

from django.db.models import QuerySet


class DiscountInterface(ABC):
    """
    Интерфейс для работы со скидками
    """

    @abstractmethod
    def get_discount_by_product_or_category(self, product: Product,
                                            category: Category) \
            -> ProductDiscount:
        """
        Метод получения скидки на товар
        """
        pass

    @abstractmethod
    def get_discount_by_cart(self) -> CartDiscount:
        """
        Метод получения скидки на корзину
        """
        pass

    @abstractmethod
    def get_set_discounts_for_product(
            self, product: Product) -> QuerySet[SetDiscount]:
        """
        Получить все скидки на наборы, в которых есть данный продукт
        """
        pass

    @abstractmethod
    def get_set_discounts_all(self) -> QuerySet[SetDiscount]:
        """
        Получить все скидки на наборы, которые
        действуют сейчас или будет действовать
        в будущем
        """
        pass

    @abstractmethod
    def get_cart_discounts_all(self) -> QuerySet[CartDiscount]:
        """
        Получить все скидки на корзину, которые
        действуют сейчас или будет действовать
        в будущем
        """
        pass

    @abstractmethod
    def get_products_discounts_all(self) -> QuerySet[ProductDiscount]:
        """
        Получить все скидки на товары, которые
        действуют сейчас или будет действовать
        в будущем
        """
        pass
