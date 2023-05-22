from django.db import models
from coreapp.models import BaseModel
from authapp.models import User
from productsapp.models.product import Product
from coreapp.enums import ORDER_STATUSES
from django.utils.translation import gettext_lazy as _


class Order(BaseModel):
    """
    Класс модели заказа
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='orders'
    )
    status = models.CharField(
        max_length=20,
        verbose_name=_('status'),
        choices=ORDER_STATUSES
    )

    def __str__(self):
        return f'Order {self.id}'

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class OrderItem(BaseModel):
    """
    Класс модели товара в заказе
    """
    order = models.ForeignKey(
        Order,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name=_('order item'))
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product'),
        related_name='ordered')
    count = models.PositiveSmallIntegerField(
        verbose_name=_('count'))
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('price'))

    def __str__(self):
        return f'{self.product} x{self.count}'

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')
