from django.db.models import QuerySet, Sum, F
from django.shortcuts import get_object_or_404

from authapp.models import User

from cartapp.models.cart import Cart
from cartapp.models.cartitem import CartItem

from productsapp.models.product import Product

from interfaces.cart_interface import CartInterface, CartItemInterface


class RepCart(CartInterface):
    def get_cart(self, user: User) -> Cart:
        """
        Возвращает корзину пользователя user
        """
        cart = get_object_or_404(Cart, user=user)
        return cart

    def get_all_carts(self) -> QuerySet[Cart]:
        """
        Возвращает все корзины
        """
        carts = Cart.objects.all()
        return carts

    def get_total_amount(self, cart: Cart) -> float:
        """
        Общая стоимость
        """
        total_amount = cart.cartitems.aggregate(
            total_amount=Sum(F('product__price') * F('quantity'))
        )
        # Доделать позже
        return total_amount

    # return self.items.aggregate(
    #     total_amount=Sum(F('product__price') * F('quantity'))
    # )['total_amount']
    def count_items(self, cart: Cart) -> int:
        """
        Количество позиций
        """
        # Доделать позже
        return cart.cartitems.count()

    #     return self.items.count()
    def save(self, force=None, **kwargs) -> Cart:
        """
        Создание или обновление корзины
        """
        if force:
            cart = force
            for key, value in kwargs:
                cart.key = value
            cart.save()
            return cart
        else:
            cart = Cart.objects.create(**kwargs)
            return cart

    def delete(self, cart: Cart) -> None:
        """
        Удаление корзины
        """
        cart.delete()


class RepCartItem(CartItemInterface):

    def get_all_items(self, cart: Cart) -> QuerySet[CartItem]:
        """
        Метод возвращает все товары в корзине
        """
        cart_items = CartItem.objects.filter(cart=cart).\
            select_related('product')
        return cart_items

    def get_cart_item(self, cart: Cart, product: Product) \
            -> QuerySet[CartItem]:
        """
        Возвращает одну позицию товара
        """
        cart_item = CartItem.objects. \
            select_related('product'). \
            filter(cart=cart, product=product)
        return cart_item

    def save(self, force=None, **kwargs) -> CartItem:
        """
        Создание или обновление позиции с товаром
        """
        if force:
            cart_item = force
            for key in kwargs:
                cart_item.key = kwargs[key]
            cart_item.save()
            return cart_item
        else:
            cart_item = CartItem.objects.create(**kwargs)
            return cart_item

    def delete(self, cart_item: QuerySet[CartItem]) -> None:
        """
        Удаление всей позиции с товаром
        """
        cart_item.delete()
