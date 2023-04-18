from django.db import models
from coreapp.models import BaseModel
from taggit.managers import TaggableManager

from authapp.models import User


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
                            verbose_name="name")
    start_date = models.DateTimeField(blank=True,
                                      null=False)
    expiration_date = models.DateTimeField(blank=True,
                                           null=True)
    description = models.TextField(null=True,
                                   blank=True,
                                   verbose_name="description")

    def __str__(self):
        return self.name


class Comment(BaseModel):
    """
    Класс-модель для комментариев
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="comments")
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="comments")
    name = models.CharField(max_length=100,
                            blank=True,
                            null=False,
                            verbose_name="name")
    text = models.TextField(blank=True,
                            null=False,
                            verbose_name="text")

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"

    def __str__(self):
        return self.name
