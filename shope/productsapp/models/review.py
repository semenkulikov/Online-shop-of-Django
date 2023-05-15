from django.db import models
from coreapp.models import BaseModel

from productsapp.models.product import Product
from profileapp.models import Profile


class Review(BaseModel):
    """
    Класс-модель для комментариев
    """
    user = models.ForeignKey(Profile,
                             on_delete=models.CASCADE,
                             related_name="reviews")
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="review")
    text = models.TextField(blank=True,
                            null=False,
                            verbose_name="text")

    class Meta:
        verbose_name = "review"
        verbose_name_plural = "reviews"

    def __str__(self):
        return f"Reviews from {self.user.user.first_name}"
