# flake8: noqa
from django.db import models

from coreapp.models import BaseModel
from cartapp.models.cart import Cart
from productsapp.models.product import Product
from productsapp.models.seller import Seller


class CartItem(BaseModel):
    """
    CartItems model
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cartitems',
        verbose_name='product'
    )
    quantity = models.PositiveIntegerField(
        null=False,
        default=1,
        verbose_name='quantity'
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='cart'
    )
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='seller'
    )

    class Meta:
        verbose_name_plural = 'items in cart'
        verbose_name = 'item in cart'

    def __str__(self):
        return f'{self.product} ({self.quantity})' \
            # f' {self.quantity * self.product.price}'

    # @property
    # def total(self):
    #     return self.product.price * self.quantity
