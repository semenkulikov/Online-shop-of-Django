from repositories.cart_repository import RepCart, RepCartItem
from repositories.seller_select_repository import SellerSelectRepository
from repositories.product_select_repository import ProductSelectRepository
from repositories.price_repository import PriceRepository

rep_cart = RepCart()
rep_cart_item = RepCartItem()
rep_seller = SellerSelectRepository()
rep_prod = ProductSelectRepository()
rep_price = PriceRepository()


class SelectCart:
    """
    Сервис получения информации о корзине пользователя
    """

    @classmethod
    def cart_items_list(cls, user=None, session_products=None):
        """
        Получение списка товаров в корзине
        Если пользователь авторизован, то методу
        передаётся экземпляр пользователя
        Если не авторизован, то передаётся словарь:
        session_products =
        {'product_id seller_id': count,...}
        """
        items_list = []
        if user:  # пользователь авторизован
            cart = rep_cart.get_cart(user)
            # корзина пользователя user
            items_list = rep_cart_item.get_all_items(cart)
            # список товаров в корзине
        else:  # есть товары в сессии
            for item in session_products:
                # цикл по ключам "product_id" и "seller_id" в сессии
                product_id, seller_id = item.split()[0], item.split()[1]
                product = rep_prod. \
                    get_product_by_id(product_id)  # продукт
                seller = rep_seller. \
                    get_seller(seller_id)  # продавец
                items_list.append(rep_price.get_object_price(product, seller))
        return items_list

    @classmethod
    def cart_all_products_amount(cls, cart=None, session_products=None):
        """
        Получение общего количества товаров в корзине
        если есть товары в сессии, то в метод передаётся словарь
        session_products =
        {'product_id seller_id': count,...}
        """
        if cart:
            # в метод передан экземпляр пользователя(авторизован)
            count = rep_cart.count_items(cart)
        elif session_products:
            # в метод передан словарь <session_products>
            count = sum([count for count in
                         session_products.values()])
        else:
            count = 0
        return count

    @classmethod
    def cart_items_amount(cls, cart=None, session_products=None):
        """
        Получение общего количества позиций с товарами в корзине
        если есть товары в сессии, то в метод передаётся словарь
        session_products =
        {'product_id seller_id': count,...}
        """
        if cart:
            # в метод передан экземпляр пользователя(авторизован)
            count = rep_cart_item.get_count_cart_items(cart)
        elif session_products:
            # в метод передан словарь <session_products>
            count = len(session_products)
        else:
            count = 0
        return count

    @classmethod
    def cart_total_amount(cls, cart=None, session_products=None):
        """
        Получение общей цены товаров в корзине
        если есть товары в сессии, то в метод передаётся словарь
        session_products =
        {'product_id seller_id': count,...}
        """
        if cart:
            # в метод передан экземпляр корзины пользователя(авторизован)
            total_amount = rep_cart.get_total_amount(cart)
            # общая сумма
        elif session_products:
            # в метод передан словарь <session_products>
            cart_sum = []
            for item in session_products:
                product_id, seller_id = item.split()[0], item.split()[1]
                cart_sum.append(
                    rep_price.
                    get_price(product=rep_prod.
                              get_product_by_id(product_id),
                              seller=rep_seller.
                              get_seller(seller_id))
                    * session_products[f'{product_id} {seller_id}'])
                #  сумма товаров в корзине,
                #  с помощью цикла берутся product_id, seller_id, count
                #  из сессии
            total_amount = sum(cart_sum)
        else:
            total_amount = 0
        return total_amount
