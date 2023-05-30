from abc import ABC, abstractmethod
from orderapp.models import Order
from authapp.models import User


class OrderUpdateInterface(ABC):

    @abstractmethod
    def create(self, user: User) -> Order:
        """Создать новый заказ"""
        pass
