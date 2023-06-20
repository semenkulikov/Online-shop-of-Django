from repositories import ProductSelectRepository, DiscountRepository, \
    PriceRepository, SellerSelectRepository
from repositories.cart_repository import RepCartItem
from typing import List
from cartapp.models import CartItem

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
        Метод возвращает список цен на товары в корзине с учетом скидки
        """
        cart_prices = []
        if cart:  # пользователь авторизован
            items = cartitem_rep.get_all_items(cart)
            #  все cart_items которые есть в корзине
            for item in items:
                #  цикл по каждой позиции с товаром в корзине
                category = item.product.category
                discount = cls.get_priority_product_discount(item.product,
                                                             category)
                # приоритетная скидка на товар или его категорию
                price = item.price
                if discount:
                    # если скидка на товар есть, то считается цена со
                    # скидкой
                    discounted_price = (price - price * discount.value / 100)
                    price = round(float(discounted_price * item.quantity), 2)
                else:
                    # цена без скидки
                    price = round(float(item.price * item.quantity), 2)
                item.discounted_price = price
                cart_prices.append(price)
            # обновление поля discounted_price во всех позициях с товарами
            # в корзине
            CartItem.objects.bulk_update(
                items, ['discounted_price'], batch_size=20
            )

        else:  # пользователь не авторизован
            for item in session_products:
                # цикл по товарам в словаре session_products
                product = rep_prod.get_product_by_id(item.split()[0])
                seller = rep_seller.get_seller(item.split()[1])
                price = rep_price.get_price(product=product,
                                            seller=seller)
                discount = cls.get_priority_product_discount(product,
                                                             product.category)
                # приоритетная скидка на товар
                if discount:
                    # если скидка есть, то рассчитывается цена со скидкой
                    price = round(float((price - price * discount.value / 100)
                                        * session_products[item]), 2)
                else:
                    # цена без скидки
                    price = round(float(price * session_products[item]), 2)
                cart_prices.append(price)
        return cart_prices

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
        Метод возвращает список цен на каждый товар
        в корзине со скидкой
        """
        products_discounted = set_discount.products.all()
        cart_prices = []
        if cart:  # пользователь авторизован
            items = cartitem_rep.get_all_items(cart)
            for item in items:
                price = item.price
                if item.product in products_discounted:
                    # если товар есть в скидочном наборе,
                    # то на него действует скидка
                    discounted_price = (price - price *
                                        set_discount.value / 100)
                    price = float(discounted_price * item.quantity)
                else:
                    # цена без скидки
                    price = item.price * item.quantity
                item.discounted_price = price
                cart_prices.append(price)
            # обновление поля discounted_price во всех позициях с товарами
            # в корзине
            CartItem.objects.bulk_update(
                items, ['discounted_price'], batch_size=20
            )

        else:  # пользователь не авторизован
            for item in session_products:
                product = rep_prod.get_product_by_id(item.split()[0])
                seller = rep_seller.get_seller(item.split()[1])
                price = rep_price.get_price(product=product,
                                            seller=seller)
                if product in products_discounted:
                    # товар находится в скидочном наборе
                    # на него действует скидка
                    price = float((price - price *
                                   set_discount.value / 100) *
                                  session_products[item])
                else:
                    # у товара нет скидки
                    price = float(price * session_products[item])
                cart_prices.append(price)
        return cart_prices

    @classmethod
    def apply_cart_discount(cls, cart_discount, cart_price,
                            cart=None, session_products=None, ):
        """
        Метод применяет скидку на корзину
        и возвращает список цен на товары в корзине
        """
        discount = cart_discount.value
        cart_prices = []
        if cart:  # пользователь авторизован
            items = cartitem_rep.get_all_items(cart)
            for item in items:
                price = item.price
                discounted_price = (price - price * discount / 100)
                price = float(discounted_price * item.quantity)
                item.discounted_price = price
                cart_prices.append(price)
            # обновление поля discounted_price во всех позициях с товарами
            # в корзине
            CartItem.objects.bulk_update(
                items, ['discounted_price'], batch_size=20
            )
        else:  # пользователь не авторизован
            for item in session_products:
                product = rep_prod.get_product_by_id(item.split()[0])
                seller = rep_seller.get_seller(item.split()[1])
                price = rep_price.get_price(product=product,
                                            seller=seller)
                price = float((price - price * discount / 100) *
                              session_products[item])
                cart_prices.append(price)
        return cart_prices

    @classmethod
    def get_prices_discount_on_cart(cls, cart_price, count,
                                    cart=None, session_products=None):
        """
        В методе происходит определение наиболее приоритетной схемы скидки
        Если пользователь авторизован, то в метод передаётся
        экземпляр корзины пользователя - cart, если нет, то словарь
        session_products =
        {'product_id seller_id': count,...}
        Метод возвращает список цен на товары в корзине
        """

        if cart:  # пользователь авторизован
            products_id = product_repository.get_products_id_from_cart(cart)
            cart_discount = cls. \
                get_priority_cart_discount(cart_price, count)
            # скидка на корзину
            set_discount = cls. \
                get_priority_set_discount(products_id)
            # скидка на набор
            if cart_discount and set_discount:
                #  имеется скидка и на корзину, и есть набор товаров
                if cart_discount.priority >= set_discount.priority:
                    # приоритет скидки на корзину выше либо равен
                    # приоритету скидки на набор товаров
                    cart_prices_list = cls. \
                        apply_cart_discount(cart_discount, cart_price,
                                            cart=cart)
                    # применение скидки на корзину
                else:
                    cart_prices_list = cls. \
                        apply_set_discount(set_discount, cart=cart)
                    # применение скидки на набор товаров
            elif cart_discount:
                # имеется только скидка на корзину
                cart_prices_list = cls. \
                    apply_cart_discount(cart_discount, cart_price,
                                        cart=cart)
            elif set_discount:
                # имеется только скидка на набор товаров
                cart_prices_list = cls. \
                    apply_set_discount(set_discount, cart=cart)
            else:
                # скидки на корзину и набор отсутствуют,
                # идет подсчет скидки на каждый товар
                cart_prices_list = cls. \
                    apply_products_discount(cart)
        elif session_products:
            # есть товары в сессии(пользователь не авторизован)
            # логика та же, что и при авторизованном
            products_id = [item.split()[0] for item in session_products.keys()]
            cart_discount = cls. \
                get_priority_cart_discount(cart_price, count)
            set_discount = cls. \
                get_priority_set_discount(products_id)
            if cart_discount and set_discount:
                if cart_discount.priority >= set_discount.priority:
                    cart_prices_list = cls. \
                        apply_cart_discount(cart_discount,
                                            cart_price,
                                            session_products=session_products)
                else:
                    cart_prices_list = cls. \
                        apply_set_discount(set_discount,
                                           session_products=session_products)
            elif cart_discount:
                cart_prices_list = cls. \
                    apply_cart_discount(cart_discount,
                                        cart_price,
                                        session_products=session_products)
            elif set_discount:
                cart_prices_list = cls. \
                    apply_set_discount(set_discount,
                                       session_products=session_products)
            else:
                cart_prices_list = cls. \
                    apply_products_discount(session_products=session_products)
        else:
            cart_prices_list = []
        return cart_prices_list
