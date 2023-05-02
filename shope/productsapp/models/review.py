from django.db import models
from coreapp.models import BaseModel

from authapp.models import User
from productsapp.models.product import Product


class Review(BaseModel):
    """
    Класс-модель для комментария
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="reviews")
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="reviews")
    text = models.TextField(blank=True,
                            null=False,
                            verbose_name="text")

    class Meta:
        verbose_name = "review"
        verbose_name_plural = "reviews"

    def __str__(self):
        return self.name
