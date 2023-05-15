from abc import ABC, abstractmethod
from productsapp.models import Product


class PriceInterface(ABC):

    @classmethod
    @abstractmethod
    def get_avg_prices(cls, product: Product) -> int:
        """
        Получить среднее значение цен конкретного продукта

        :param product: продукт, у которого нужно узнать цену

        :return: усредненная цена
        """
        pass
