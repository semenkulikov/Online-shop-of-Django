from django.db import models
from coreapp.models import BaseModel
from taggit.managers import TaggableManager

from productsapp.models import Category


class Product(BaseModel):
    """
    Класс модель для продуктов
    """
    name = models.CharField(verbose_name="name",
                            max_length=100)
    description = models.TextField(verbose_name="description",
                                   null=False,
                                   blank=True)
    image = models.ImageField(upload_to="products", null=True,
                              verbose_name="image")
    tags = TaggableManager()
    archived = models.BooleanField(default=False,
                                   verbose_name="archived")
    is_delivered = models.BooleanField(default=False,
                                       verbose_name="is_delivered")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="product", null=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return self.name
