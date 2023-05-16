from django.db.models import Avg

from interfaces.price_interface import PriceInterface
from productsapp.models import Product, SlicePrice


class PriceRepository(PriceInterface):

    def get_avg_prices(self, product: Product) -> int:
        average_price = SlicePrice.objects.filter(
            product=product
        ).aggregate(
            price=Avg("value")
        )
        return average_price.get("price")
