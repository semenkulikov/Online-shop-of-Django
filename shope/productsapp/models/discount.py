from django.db import models
from coreapp.models import BaseModel
from productsapp.models.product import Product
from django.utils.translation import gettext_lazy as _


class Discount(BaseModel):
    """
    Класс-модель для продуктов со скидками
    """
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="discounted_products")
    name = models.CharField(max_length=100,
                            blank=True,
                            null=False,
                            verbose_name=_("name"))
    start_date = models.DateTimeField(blank=True,
                                      null=False)
    expiration_date = models.DateTimeField(blank=True,
                                           null=True)
    description = models.TextField(null=True,
                                   blank=True,
                                   verbose_name=_("description"))

    def __str__(self):
        return self.name
