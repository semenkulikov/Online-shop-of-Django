from django.db import models
from coreapp.models import BaseModel


class Category(BaseModel):
    """
    Класс-модель для определения категории продукта
    """
    name = models.CharField(max_length=100,
                            null=False,
                            blank=True,
                            verbose_name="name")

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
