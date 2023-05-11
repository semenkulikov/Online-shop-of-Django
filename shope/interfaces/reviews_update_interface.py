from abc import ABC, abstractmethod

from productsapp.models import Review


class ReviewUpdateInterface(ABC):

    @abstractmethod
    def update_review(self, review: Review, force=None) -> None:
        """ Обновление или создание отзыва """
        pass
