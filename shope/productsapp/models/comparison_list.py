from django.db import models
from productsapp.models import Product


class ComparisonList(models.Model):
    products = models.ForeignKey(Product,
                                 on_delete=models.DO_NOTHING,
                                 related_name="comparison_list")
