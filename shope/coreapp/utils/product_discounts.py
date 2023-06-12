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
    def get_discounted_cart_price(cls, cart_price, count):
        """
        Получение приоритетной скидки на корзину
        Возвращает экземпляр CartDiscount, если есть скидка на
        корзину и необходимые условия для скидки выполнены
        """
        discount = discount_rep.get_discount_by_cart()
        discount_conditions = False
        # выполнены ли условия для скидки
        if not discount:
            # если скидки на корзину отсутствуют
            return False
        # скидка на корзину
        if discount.required_sum and discount.required_quantity:
            # есть оба условия для получения скидки
            # необходимая сумма и необходимое количество
            if cart_price >= discount.required_sum \
                    and count >= discount.required_quantity:
                # сумма корзины и количество позиций с товарами
                # удовлетворяют условиям
                discount_conditions = discount
        elif discount.required_sum \
                and not discount.required_quantity:
            # условие одно - сумма корзины
            if cart_price >= discount.required_sum:
                discount_conditions = discount
        elif discount.required_quantity \
                and not discount.required_sum:
            # условие одно - количество товаров
            if count >= discount.required_quantity:
                discount_conditions = discount
        return discount_conditions

    @classmethod
    def get_discounted_set_price(cls):
        """
        Получить скидку на набор товаров
        """
        pass
