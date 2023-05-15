from django.db.models import QuerySet, Sum, F
from django.shortcuts import get_object_or_404

from authapp.models import User

from cartapp.models.cart import Cart
from cartapp.models.cartitem import CartItem

from productsapp.models.product import Product

from interfaces.cart_interface import CartInterface, CartItemInterface


class RepCart(CartInterface):
    @classmethod
    def get_cart(cls, user: User) -> Cart:
        """
        Возвращает корзину пользователя user
        """
        cart = get_object_or_404(Cart, user=user)
        return cart

    @classmethod
    def get_all_carts(cls) -> QuerySet[Cart]:
        """
        Возвращает все корзины
        """
        carts = Cart.objects.all()
        return carts

    @classmethod
    def get_total_amount(cls, cart: Cart) -> float:
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
    @classmethod
    def count_items(cls, cart: Cart) -> int:
        """
        Количество товаров в корзине
        """
        total_products = cart.items. \
            aggregate(Sum('quantity'))['quantity__sum']
        return total_products

    @classmethod
    def save(cls, force=None, **kwargs) -> Cart:
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

    @classmethod
    def delete(cls, cart: Cart) -> None:
        """
        Удаление корзины
        """
        cart.delete()


class RepCartItem(CartItemInterface):
    @classmethod
    def get_all_items(cls, cart: Cart) -> QuerySet[CartItem]:
        """
        Метод возвращает все товары в корзине
        """
        cart_items = CartItem.objects.filter(cart=cart). \
            select_related('product')
        return cart_items

    @classmethod
    def get_cart_item(cls, cart: Cart, product: Product) \
            -> QuerySet[CartItem]:
        """
        Возвращает одну позицию товара
        """
        cart_item = CartItem.objects. \
            select_related('product'). \
            filter(cart=cart, product=product)
        return cart_item

    @classmethod
    def save(cls, force=None, **kwargs) -> CartItem:
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

    @classmethod
    def delete(cls, cart_item: QuerySet[CartItem]) -> None:
        """
        Удаление всей позиции с товаром
        """
        cart_item.delete()
