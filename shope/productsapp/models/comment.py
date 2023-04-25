from django.db import models
from coreapp.models import BaseModel

from authapp.models import User
from productsapp.models.product import Product


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
        verbose_name = "review"
        verbose_name_plural = "reviews"

    def __str__(self):
        return self.name
