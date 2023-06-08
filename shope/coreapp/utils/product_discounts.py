from repositories.product_select_repository import ProductSelectRepository
from repositories.discount_select_repository import DiscountRepository

_product_repository = ProductSelectRepository()
discount_rep = DiscountRepository()


class ProductDiscounts:
    """
    Сервис получения скидок на товары
    """

    @classmethod
    def get_discounted_price_on_product(cls, price, product, category):
        """
        Рассчитать скидку на товар или категорию.
        Возвращает цену на товар/категорию со скидкой
        """
        discount = discount_rep. \
            get_discount_by_product_or_category(product=product,
                                                category=category)
        price -= price * discount / 100
        return price

    @classmethod
    def get_discounted_cart_price(cls, cart_price):
        """
        Рассчитать цену корзины с учётом скидки
        """

    @classmethod
    def get_discounted_set_price(cls):
        """
        Получить скидку на набор товаров
        """
