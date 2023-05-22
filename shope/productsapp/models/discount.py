from django.db import models
from coreapp.models import BaseModel
from productsapp.models.product import Product, Category


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


class ProductDiscount(BaseDiscount):
    """ Класс-модель скидки для списка продуктов и категорий"""
    products = models.ManyToManyField(
        Product,
        related_name='product_discounts',
        verbose_name='products')
    categories = models.ManyToManyField(
        Category,
        related_name='category_discounts')


class CartDiscount(BaseDiscount):
    """Класс-модель скидки на корзину товаров"""
    required_sum = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2,
        verbose_name='required sum')
    required_quantity = models.PositiveSmallIntegerField(
        null=False,
        blank=True,
        verbose_name='required quantity')
