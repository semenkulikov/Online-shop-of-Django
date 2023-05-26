from django.db.models import Avg
from interfaces.price_interface import PriceInterface
from productsapp.models import Product, SlicePrice, Seller


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
        Метод возвращает последнее значение цены на продукт,
        установленную продавцом.
        """
        price = SlicePrice.objects.order_by('-updated_at'). \
            filter(seller=seller, product=product).first().value
        return price

    def get_object_price(self, product: Product, seller: Seller) -> SlicePrice:
        """
        Метод возвращает объект SlicePrice
        """
        price_object = SlicePrice.objects. \
            select_related('seller', 'product'). \
            order_by('-updated_at'). \
            filter(product=product, seller=seller).first()
        return price_object
