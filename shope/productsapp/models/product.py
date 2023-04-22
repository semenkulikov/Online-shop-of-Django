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
    price = models.DecimalField(default=0,
                                max_digits=8,
                                decimal_places=2,
                                verbose_name="price")
    image = models.ImageField(upload_to="products",
                              verbose_name="image")
    tags = TaggableManager()
    archived = models.BooleanField(default=False,
                                   verbose_name="archived")
    is_delivered = models.BooleanField(default=False,
                                       verbose_name="is_delivered")
    # category = models.ForeignKey()
    # specifics = models.ForeignKey()

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = "-price", "name", "archived", "is_delivered"

    def __str__(self):
        return self.name
