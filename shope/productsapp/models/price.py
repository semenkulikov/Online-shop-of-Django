from django.db import models

from coreapp.models import BaseModel
from productsapp.models import Product


class Price(BaseModel):
    """ Класс-модель для цены """
    value = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name="price")

    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="amount")

    def __str__(self):
        return f"{self.product.name} - {self.value}"

    class Meta:
        verbose_name = "price"
        verbose_name_plural = "prices"
