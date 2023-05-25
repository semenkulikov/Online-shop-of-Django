from django.db.models import Avg

from interfaces.price_interface import PriceInterface
from productsapp.models import Product, SlicePrice, Seller
from django.shortcuts import get_object_or_404


class PriceRepository(PriceInterface):

    def get_avg_prices(self, product: Product) -> int:
        average_price = SlicePrice.objects.filter(
            product=product
        ).aggregate(
            price=Avg("value")
        )
        return average_price.get("price")

    def get_price(self, product: Product, seller: Seller) -> float:
        """
        Метод возвращает значение цены на продукт, установленную продавцом.
        """
        price = get_object_or_404(SlicePrice, product=product,
                                  seller=seller).value
        return price
