from django.db.models import QuerySet

from interfaces.sellers_select_interface import SellerSelectInterface
from productsapp.models import Product, Seller

from django.db.models import F


class SellerSelectRepository(SellerSelectInterface):

    def get_seller_by_product(self, product: Product) -> QuerySet[Seller]:
        sellers = Seller.objects.filter(
            seller_items__product=product
        ).annotate(price=F('slice_price__value'))
        return sellers

    def get_all_sellers(self) -> QuerySet[Seller]:
        pass
