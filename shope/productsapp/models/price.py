from django.db import models

from coreapp.models import BaseModel
from productsapp.models import Product


class Price(BaseModel):
    """ Класс-модель для цены """
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name="price")
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="price")

    def __str__(self):
        return f"{self.product.name} - {self.price}"

    class Meta:
        verbose_name = "price"
        verbose_name_plural = "prices"
