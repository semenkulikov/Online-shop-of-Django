from django.db import models

from coreapp.models import BaseModel
from productsapp.models import Product, Seller


class SlicePrice(BaseModel):
    """
    Класс-модель для цены
    """
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='value'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_price',
        verbose_name='product'
    )

    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='slice_price',
        verbose_name='seller'
    )

    def __str__(self):
        return f"{self.product} - {self.seller} - {self.value}"

    class Meta:
        verbose_name = "price slice"
        verbose_name_plural = "price slices"
