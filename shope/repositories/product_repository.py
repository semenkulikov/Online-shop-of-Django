from typing import List

from django.db.models import QuerySet

from interfaces.product_interface import ProductInterface
from productsapp.models import Product


class ProductRepository(ProductInterface):

    def get_products_with_these_id(self, products_id: List[int])\
            -> QuerySet[Product]:
        return Product.objects.filter(id__in=products_id)
