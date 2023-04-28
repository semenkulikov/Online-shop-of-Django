from django.db import models

from coreapp.models import BaseModel


class Seller(BaseModel):
    """
    Класс-модель продавца
    """
    name = models.CharField(
        max_length=100,
        verbose_name='name'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "seller"
        verbose_name_plural = "sellers"
