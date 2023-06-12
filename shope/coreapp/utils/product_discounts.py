from repositories.product_select_repository import ProductSelectRepository
from repositories.discount_select_repository import DiscountRepository
from repositories.cart_repository import RepCartItem
from typing import List

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
        Получение приоритетной скидки на корзину.
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

    @classmethod
    def get_priority_set_discount(cls, products_id: List[int]):
        """
        Проверить корзину на наличе скидочных наборов
        и вернуть скидку на приоритетный набор
        """
        # множество товаров, содержащихся в позициях корзины
        cart_prod_set = set(
            product_repository.get_products_with_these_id(products_id))

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
