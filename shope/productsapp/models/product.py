from django.db import models
from coreapp.models import BaseModel
from taggit.managers import TaggableManager


class Product(BaseModel):
    """
    Класс модель для продуктов
    """
    name = models.CharField(verbose_name="name",
                            max_length=100)
    description = models.TextField(verbose_name="description",
                                   null=False,
                                   blank=True)

    image = models.ImageField(upload_to="products",
                              verbose_name="image")
    tags = TaggableManager()
    archived = models.BooleanField(default=False,
                                   verbose_name="archived")
    is_delivered = models.BooleanField(default=False,
                                       verbose_name="is_delivered")

    category = models.ForeignKey(
        'productsapp.Category',
        on_delete=models.DO_NOTHING,
        verbose_name='category',
        related_name='category_products'
    )

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return self.name
