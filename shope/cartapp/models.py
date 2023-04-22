from django.db import models

from authapp.models import User
from coreapp.models import BaseModel
from productsapp.models.product import Product

from django.db.models import Sum, F


class Cart(BaseModel):
    """
    Cart model
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return f'{self.user} cart - {self.total_amount}'

    @property
    def total_amount(self):
        return self.items.aggregate(
            total_amount=Sum(F('product__price') * F('quantity'))
        )['total_amount']

    @property
    def count_items(self):
        return self.items.count()


class CartItem(BaseModel):
    """
    CartItems model
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cartitems',
        verbose_name='продукт'
    )
    quantity = models.PositiveIntegerField(
        null=False,
        default=0,
        verbose_name='количество'
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='корзина'
    )

    class Meta:
        verbose_name_plural = 'позиции в корзине'
        verbose_name = 'позиция в корзине'

    def __str__(self):
        return f'{self.product} ({self.quantity})' \
               f' {self.quantity * self.product.price}'

    # @property
    # def total(self):
    #     return self.product.price * self.quantity
