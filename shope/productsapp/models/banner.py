from django.db import models
from coreapp.models import BaseModel
from productsapp.models import Category


class Banner(BaseModel):
    """
    Класс-модель баннеров на главной странице
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='category',
        related_name='banner'
    )

    image = models.ImageField(
        upload_to='banners_images/',
        verbose_name='image'
    )

    class Meta:
        verbose_name = "banner"
        verbose_name_plural = "banners"

    def __str__(self):
        return self.category.name

    @property
    def category_min_price(self):
        return None
