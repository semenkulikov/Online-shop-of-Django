from abc import ABC, abstractmethod
from django.db.models import QuerySet

from authapp.models import User

from cartapp.models.cart import Cart
from cartapp.models.cartitem import CartItem


class CartInterface(ABC):
    @abstractmethod
    def get_cart(self, user: User) -> QuerySet[Cart]:
        pass

    @abstractmethod
    def get_all_carts(self) -> QuerySet[Cart]:
        pass

    @abstractmethod
    def get_total_amount(self, cart: Cart) -> float:
        pass

    # return self.items.aggregate(
    #     total_amount=Sum(F('product__price') * F('quantity'))
    # )['total_amount']
    @abstractmethod
    def count_items(self, cart: Cart) -> int:
        pass

    #     return self.items.count()

    @abstractmethod
    def save(self, force=None, **kwargs):
        if force:
            pass

    @abstractmethod
    def delete(self, cart: Cart) -> None:
        pass


class CartItemInterface(ABC):
    @abstractmethod
    def get_all_items(self, cart: Cart) -> QuerySet[CartItem]:
        pass

    @abstractmethod
    def get_cart_item(self, cart: Cart, product_id: int) -> QuerySet[CartItem]:
        pass

    @abstractmethod
    def save(self, force, **kwargs):
        if force:
            pass

    @abstractmethod
    def delete(self, cart_item: CartItem) -> None:
        pass
