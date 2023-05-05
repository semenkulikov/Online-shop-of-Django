from django.db import models

from coreapp.models import BaseModel
from productsapp.models import Seller, Product


class SellerItem(BaseModel):
    """
    Класс-модель товара у продавца
    """
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='seller_items',
        verbose_name='seller'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='seller_items',
        verbose_name='product'
    )

    def __str__(self):
        return f'{self.seller} {self.product} '

    class Meta:
        verbose_name = "seller's item"
        verbose_name_plural = "seller's items"
