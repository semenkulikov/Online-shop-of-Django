from django.db.models import Avg

from interfaces.price_interface import PriceInterface
from productsapp.models import Product, SlicePrice


class PriceRepository(PriceInterface):

    @classmethod
    def get_avg_prices(cls, product: Product) -> int:
        average_price = SlicePrice.objects.filter(
            product=product
        ).aggregate(
            price=Avg("value")
        )
        return average_price.get("price")
