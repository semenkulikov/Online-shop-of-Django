from repositories import ProductSelectRepository, DiscountRepository, \
    PriceRepository, SellerSelectRepository
from repositories.cart_repository import RepCartItem
from typing import List

product_repository = ProductSelectRepository()
discount_rep = DiscountRepository()
cartitem_rep = RepCartItem()
rep_price = PriceRepository()
rep_prod = ProductSelectRepository()
rep_seller = SellerSelectRepository()


class ProductDiscounts:
    """
    Сервис получения скидок на товары
    """

    @classmethod
    def get_priority_product_discount(cls, product, category):
        """
        Метод возвращает приоритетную скидку на товар или категорию
        """
        discount = discount_rep. \
            get_discount_by_product_or_category(product=product,
                                                category=category)
        return discount

    @classmethod
    def get_priority_cart_discount(cls, cart_price, count):
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
    def get_priority_set_discount(cls, products_id: List[int]):
        """
        Проверить корзину на наличие скидочных наборов
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
        if result_discounts:
            priority_discount = max(result_discounts,
                                    key=lambda discount: discount.priority)
        else:
            return None
        return priority_discount

    @classmethod
    def apply_products_discount(cls, cart=None, session_products=None):
        """
        Метод применяет скидку к каждому товару и
        возвращает цену на корзину с применённой скидкой
        Если пользователь авторизован, то в метод передаётся
        экземпляр корзины пользователя - cart, если нет, то словарь
        session_products =
        {'product_id seller_id': count,...}
        Метод возвращает сумму товаров в корзине со скидкой
        """
        cart_sum = []
        if cart:
            items = cartitem_rep.get_all_items(cart)
            for item in items:
                category = item.product.category
                discount = cls.get_priority_product_discount(item.product,
                                                             category)
                price = item.price
                if discount:
                    price = (price - price * discount.value / 100) * \
                            item.quantity
                else:
                    price *= item.quantity
                cart_sum.append(price)
        else:
            for item in session_products:
                product = rep_prod.get_product_by_id(item.split()[0])
                seller = rep_seller.get_seller(item.split()[1])
                price = rep_price.get_price(product=product,
                                            seller=seller)
                discount = cls.get_priority_product_discount(product,
                                                             product.category)
                if discount:
                    price = (price - price * discount.value / 100) \
                            * session_products[item]
                else:
                    price *= session_products[item]
                cart_sum.append(price)
        return sum(cart_sum)

    @classmethod
    def apply_set_discount(cls, set_discount, cart=None,
                           session_products=None):
        """
        Метод применяет скидку к набору продуктов и
        возвращает цену на корзину с применённой скидкой
        Если пользователь авторизован, то в метод передаётся
        экземпляр корзины пользователя - cart, если нет, то словарь
        session_products =
        {'product_id seller_id': count,...}
        Метод возвращает сумму товаров в корзине со скидкой
        """
        products_discounted = set_discount.products.all()
        if cart:
            cart_sum = []
            items = cartitem_rep.get_all_items(cart)
            for item in items:
                price = item.price
                if item.product in products_discounted:
                    price = (price - price * set_discount.value / 100) \
                            * item.quantity
                else:
                    price *= item.quantity
                cart_sum.append(price)
        else:
            cart_sum = []
            for item in session_products:
                product = rep_prod.get_product_by_id(item.split()[0])
                seller = rep_seller.get_seller(item.split()[1])
                price = rep_price.get_price(product=product,
                                            seller=seller)
                if product in products_discounted:
                    price = (price - price * set_discount.value / 100) * \
                            session_products[item]
                else:
                    price *= session_products[item]
                cart_sum.append(price)
        return sum(cart_sum)

    @classmethod
    def apply_cart_discount(cls, cart_discount, cart_price):
        """
        Метод применяет скидку на корзину
        и возвращает цену на корзину с примененной
        скидкой
        """
        cart_price -= cart_price * cart_discount.value / 100
        return cart_price

    @classmethod
    def get_price_discount_on_cart(cls, cart_price, count,
                                   cart=None, session_products=None):
        """
        В методе происходит определение наиболее приоритетной схемы скидки
        Если пользователь авторизован, то в метод передаётся
        экземпляр корзины пользователя - cart, если нет, то словарь
        session_products =
        {'product_id seller_id': count,...}
        Метод возвращает сумму товаров в корзине со скидкой
        """

        if cart:  # пользователь авторизован
            products_id = product_repository.get_products_id_from_cart(cart)
            cart_discount = cls.\
                get_priority_cart_discount(cart_price, count)
            # скидка на корзину
            set_discount = cls.\
                get_priority_set_discount(products_id)
            # скидка на набор
            if cart_discount and set_discount:
                #  имеется скидка и на корзину, и есть набор товаров
                if cart_discount.priority >= set_discount.priority:
                    # приоритет скидки на корзину выше либо равен
                    # приоритету скидки на набор товаров
                    total_price = cls.\
                        apply_cart_discount(cart_discount, cart_price)
                    # применение скидки на корзину
                else:
                    total_price = cls.\
                        apply_set_discount(set_discount, cart=cart)
                    # применение скидки на набор товаров
            elif cart_discount:
                # имеется только скидка на корзину
                total_price = cls.\
                    apply_cart_discount(cart_discount, cart_price)
            elif set_discount:
                # имеется только скидка на набор товаров
                total_price = cls.\
                    apply_set_discount(set_discount, cart=cart)
            else:
                # скидки на корзину и набор отсутствуют,
                # идет подсчет скидки на каждый товар
                total_price = cls.\
                    apply_products_discount(cart)
        elif session_products:
            # есть товары в сессии(пользователь не авторизован)
            # логика та же, что и при авторизованном
            products_id = [item.split()[0] for item in session_products.keys()]
            cart_discount = cls.\
                get_priority_cart_discount(cart_price, count)
            set_discount = cls.\
                get_priority_set_discount(products_id)
            if cart_discount and set_discount:
                if cart_discount.priority >= set_discount.priority:
                    total_price = cls.\
                        apply_cart_discount(cart_discount,
                                            cart_price)
                else:
                    total_price = cls.\
                        apply_set_discount(set_discount,
                                           session_products=session_products)
            elif cart_discount:
                total_price = cls.\
                    apply_cart_discount(cart_discount,
                                        cart_price)
            elif set_discount:
                total_price = cls.\
                    apply_set_discount(set_discount,
                                       session_products=session_products)
            else:
                total_price = cls.\
                    apply_products_discount(session_products=session_products)
        else:
            total_price = 0
        return round(total_price, 2)
