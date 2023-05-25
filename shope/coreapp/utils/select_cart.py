from repositories.cart_repository import RepCart, RepCartItem
from repositories.seller_select_repository import SellerSelectRepository
from repositories.product_select_repository import ProductSelectRepository
from repositories.price_repository import PriceRepository

from cartapp.models import Cart

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
        {'products': {'product_id': [count, seller_id]...}
        """
        items_list = []
        if user:  # пользователь авторизован
            cart = rep_cart.get_cart(user)
            # корзина пользователя user
            items_list = rep_cart_item.get_all_items(cart)
            # список товаров в корзине
        else:  # есть товары в сессии
            for product_id in session_products:
                # цикл по ключам "product_id" в сессии
                product = rep_prod.\
                    get_product_by_id(product_id)  # продукт
                seller = rep_seller.\
                    get_seller(session_products[product_id][1])  # продавец
                items_list.append(rep_price.get_object_price(product, seller))
        return items_list

    @classmethod
    def cart_items_amount(cls, cart: Cart):
        """
        Получение общего количества товаров в корзине
        """
        count = rep_cart.count_items(cart)
        return count

    @classmethod
    def cart_total_amount(cls, cart: Cart):
        """
        Получение суммы цен всех товаров в корзине
        """
        total_amount = rep_cart.get_total_amount(cart)
        return total_amount
