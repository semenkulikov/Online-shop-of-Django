from abc import ABC, abstractmethod

from django.db.models import QuerySet

from productsapp.models import Product, Review


class ReviewSelectInterface(ABC):

    @abstractmethod
    def get_all_reviews(self, product: Product) -> QuerySet[Review]:
        """ Получить все отзывы к продукту """
        pass

    @abstractmethod
    def get_amount_reviews(self, product: Product) -> int:
        """ Получить количество отзывов к продукту """
        pass
