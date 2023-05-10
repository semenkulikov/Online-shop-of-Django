from abc import ABC, abstractmethod
from django.db.models import QuerySet

from authapp.models import User
from orderapp.models import Order


class OrderInterface(ABC):

    @abstractmethod
    def get_all(self) -> QuerySet[Order]:
        pass

    @abstractmethod
    def get_last_activ(self, user: User) -> QuerySet[Order]:
        pass
