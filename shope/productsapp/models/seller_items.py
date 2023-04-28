from django.db import models

from coreapp.models import BaseModel
from productsapp.models import Seller, Product
from productsapp.models.price import Price


class SellerItem(BaseModel):
    """
    Класс-модель товара у продавца
    """
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='seller'
    )

    price = models.ForeignKey(
        Price,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='price'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='product'
    )

    def __str__(self):
        return f'{self.seller} {self.product} {self.price}'

    class Meta:
        verbose_name = "seller's item"
        verbose_name_plural = "seller's items"
