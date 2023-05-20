from django.db import models
from coreapp.models import BaseModel
from authapp.models import User
from productsapp.models.product import Product
from coreapp.enums import ORDER_STATUSES


class Order(BaseModel):
    """
    Класс модели заказа
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user',
        related_name='orders'
    )
    status = models.CharField(
        max_length=20,
        verbose_name='status',
        choices=ORDER_STATUSES
    )

    def __str__(self):
        return f'Order {self.id}'

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'


class OrderItem(BaseModel):
    """
    Класс модели товара в заказе
    """
    order = models.ForeignKey(
        Order,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name='order item')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='product',
        related_name='ordered')
    count = models.PositiveSmallIntegerField(
        verbose_name='count')
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='price')

    def __str__(self):
        return f'{self.product} x{self.count}'

    class Meta:
        verbose_name = 'order item'
        verbose_name_plural = 'order items'
