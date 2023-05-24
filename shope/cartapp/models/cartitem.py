# flake8: noqa
from django.db import models
from django.utils.translation import gettext_lazy as _
from coreapp.models import BaseModel
from cartapp.models.cart import Cart
from productsapp.models.product import Product


class CartItem(BaseModel):
    """
    CartItems model
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cartitems',
        verbose_name=_('product')
    )
    quantity = models.PositiveIntegerField(
        null=False,
        default=1,
        verbose_name=_('quantity')
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('cart')
    )

    class Meta:
        verbose_name_plural = _('items in cart')
        verbose_name = _('item in cart')

    def __str__(self):
        return f'{self.product} ({self.quantity})' \
               # f' {self.quantity * self.product.price}'

    # @property
    # def total(self):
    #     return self.product.price * self.quantity
