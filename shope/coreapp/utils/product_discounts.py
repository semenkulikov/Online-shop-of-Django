from repositories.product_select_repository import ProductSelectRepository
from repositories.discount_select_repository import DiscountRepository
from repositories.cart_repository import RepCartItem
from cartapp.models import Cart

product_repository = ProductSelectRepository()
discount_rep = DiscountRepository()
cartitem_rep = RepCartItem()


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
    def get_discounted_cart_price(cls, cart_price, count):
        """
        Рассчитать цену корзины с учётом скидки
        """
        pass

    @classmethod
    def get_discounted_set_price(cls):
        """
        Получить скидку на набор товаров
        """
        pass

    @classmethod
    def get_priority_set_discount(cls, cart: Cart):
        """
        Проверить корзину на наличе скидочных наборов
        и вернуть скидку на приоритетный набор
        """
        cart_items = cartitem_rep.get_all_items(cart=cart)
        # множество товаров, содержащихся в позициях корзины
        cart_prod_set = {item.product for item in cart_items}

        result_discounts = list()

        for product in cart_prod_set:
            # все скидочные наборы, где есть данный продукт
            current_discounts = discount_rep.get_set_discounts_for_product(
                product=product)

            # проверка вхождения множества товаров из набора
            # в множество товаров корзины
            for discount in current_discounts:
                disc_prod_set = set(
                    product_repository.get_products_from_set(discount))
                if disc_prod_set.issubset(cart_prod_set):
                    result_discounts.append(discount)

        priority_discount = max(result_discounts,
                                key=lambda discount: discount.priority)

        return priority_discount
