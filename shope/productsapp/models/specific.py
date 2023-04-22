from django.db import models
from coreapp.models import BaseModel
from productsapp.models.product import Product
from productsapp.models.type_spec import TypeSpecific


class Specific(BaseModel):
    """
    Класс-модель для характеристики продукта
    """
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="specific")
    description = models.TextField(null=True,
                                   blank=True,
                                   verbose_name="description")
    type_spec = models.ForeignKey(TypeSpecific,
                                  on_delete=models.CASCADE,
                                  related_name="specific")
