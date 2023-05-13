from abc import ABC, abstractmethod
from typing import List

from django.db.models import QuerySet

from productsapp.models import Product


class ProductInterface(ABC):

    @abstractmethod
    def get_products_with_these_id(self, products_id: List[int])\
            -> QuerySet[Product]:
        """ Метод для получения продуктов с заданными id """
        pass
