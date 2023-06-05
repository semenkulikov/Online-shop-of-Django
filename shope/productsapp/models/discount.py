from django.db import models
from coreapp.models import BaseModel
from productsapp.models.product import Product, Category


class BaseDiscount(BaseModel):
    """ Базовый абстрактный класс модели скидок """
    name = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        verbose_name='name')
    value = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2,
        verbose_name='value')
    start_date = models.DateField(
        null=False,
        blank=True,
        verbose_name='start date')
    expiration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='expiration date')
    description = models.CharField(
        max_length=200,
        blank=True,
        null=False,
        verbose_name='description')
    priority = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        verbose_name='priority')

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name} - {self.value} - {self.priority}'


class SetDiscount(BaseDiscount):
    """ Класс-модель скидки на фиксированный набор продуктов """
    products = models.ManyToManyField(
        Product,
        related_name='set_discounts',
        verbose_name='products')

    class Meta:
        verbose_name = "Set Discount"
        verbose_name_plural = "Set Discounts"


class ProductDiscount(BaseDiscount):
    """ Класс-модель скидки для списка продуктов и категорий"""
    products = models.ManyToManyField(
        Product,
        related_name='product_discounts',
        verbose_name='products')
    categories = models.ManyToManyField(
        Category,
        related_name='category_discounts',
        verbose_name='categories')

    class Meta:
        verbose_name = "Product Discount"
        verbose_name_plural = "Product Discounts"


class CartDiscount(BaseDiscount):
    """Класс-модель скидки на корзину товаров"""
    required_sum = models.DecimalField(
        null=False,
        max_digits=10,
        decimal_places=2,
        verbose_name='required sum')
    required_quantity = models.PositiveSmallIntegerField(
        null=False,
        blank=True,
        verbose_name='required quantity')

    class Meta:
        verbose_name = "Cart Discount"
        verbose_name_plural = "Cart Discounts"
