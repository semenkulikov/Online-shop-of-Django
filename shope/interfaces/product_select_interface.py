from abc import ABC, abstractmethod
from django.db.models import QuerySet
from productsapp.models.product import Product


class ProductSelectInterface(ABC):

    @abstractmethod
    def get_all_products(self) -> QuerySet[Product]:
        """Получить все продукты"""
        pass

    @abstractmethod
    def get_products_with_filter(self,
                                 name: str,
                                 free_shipping: bool,
                                 in_stock: bool) -> QuerySet[Product]:
        """Получить список продуктов на основании фильтра"""
        pass

    @abstractmethod
    def get_products_with_tag(self,
                              tag: str) -> QuerySet[Product]:
        """Получить список продуктов по тегу"""
        pass

    @abstractmethod
    def get_product_prices(self,
                           products: QuerySet) -> QuerySet[Product]:
        """Получить цены на список продуктов"""
        pass

    @abstractmethod
    def sort_by_popular(self,
                        products: QuerySet,
                        reverse: bool) -> QuerySet[Product]:
        """ Cортировка по количеству проданных """
        pass

    @abstractmethod
    def sort_by_reviews(self,
                        products: QuerySet,
                        reverse: bool) -> QuerySet[Product]:
        """ Cортировка по количеству отзывов """
        pass

    @abstractmethod
    def sort_by_new(self,
                    products: QuerySet,
                    reverse: bool) -> QuerySet[Product]:
        """ Cортировка по году выпуска """
        pass

    @abstractmethod
    def sort_by_price(self,
                      products: QuerySet,
                      reverse: bool) -> QuerySet[Product]:
        """ Cортировка по цене """
        pass
