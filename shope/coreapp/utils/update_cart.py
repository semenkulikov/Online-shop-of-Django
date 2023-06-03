from cartapp.models import CartItem

from django.db.models import F

from repositories.cart_repository import RepCart, RepCartItem
from repositories.seller_select_repository import SellerSelectRepository
from repositories.product_select_repository import ProductSelectRepository
from repositories.price_repository import PriceRepository

rep_cart = RepCart()
rep_cart_item = RepCartItem()
rep_seller = SellerSelectRepository()
rep_prod = ProductSelectRepository()
rep_price = PriceRepository()


class AddToCart:
    """
    Сервис добавления товара в корзину,
    удаления его из корзины и изменения
    количества товара в корзине
    """

    @classmethod
    def add_to_cart(cls, product_id, seller_id, count=1,
                    user=None, session_products=None):
        """
        Метод добавления товара в корзину
        Если есть словарь с товарами из сессии <session_products>,
        то метод вернёт обновлённый словарь для обновления текущей сессии.
        """
        if user:  # если пользователь авторизован
            product = rep_prod.get_product_by_id(product_id)  # продукт по id
            cart = rep_cart.get_cart(user)  # корзина пользователя
            seller = rep_seller.get_seller(seller_id)  # продавец по id
            cart_item = rep_cart_item.get_cart_item(cart=cart,
                                                    product=product,
                                                    seller=seller)
            # позиция с товаром в корзине
            if not cart_item:  # товара нет в корзине
                rep_cart_item.save(cart=cart, product=product,
                                   seller=seller, quantity=count)
                # создание позиции с товаром
            else:  # товар есть в корзине
                cart_item.update(quantity=F('quantity') + count)
                # добавление товаров
        else:  # анонимный пользователь
            if session_products:  # если есть товары в сессии
                # в сессии есть уже какие-либо товары
                if session_products.get(str(product_id)):
                    # позиция с товаром уже есть
                    session_products[str(product_id)][0] += count
                    # увеличить количество на count
                else:  # позиция с товаром отсутствует
                    session_products[str(product_id)] = [count, seller_id]
            else:  # в сессии нет товаров
                session_products = {str(product_id): [count, seller_id]}
            return session_products

    @classmethod
    def delete_from_cart(cls, product_id, seller_id, count=1,
                         user=None, session_products=None, full=None):
        """
        Удаление товара из корзины
        Если есть словарь с товарами из сессии <session_products>,
        то метод вернёт обновлённый словарь для обновления текущей сессии.
        """
        product = rep_prod.get_product_by_id(product_id)  # продукт по id
        seller = rep_seller.get_seller(seller_id)  # продавец по id
        if user:  # если пользователь авторизован
            cart = rep_cart.get_cart(user)  # корзина пользователя
            cart_item = rep_cart_item. \
                get_cart_item(cart=cart, product=product, seller=seller)
            # позиция с товаром в корзине
            if full or cart_item.quantity == 1:  # удаление товара из корзины
                rep_cart_item.delete(cart_item)
            else:  # уменьшение количества товара на 1
                cart_item.update(quantity=F('quantity') - count)
        else:
            if session_products:  # если есть товары в сессии
                if full or session_products[str(product_id)][0] == 1:
                    # удаление товара из корзины
                    session_products.pop(str(product_id), False)
                else:  # уменьшение количества на 1
                    session_products[str(product_id)][0] -= count
                return session_products

    @classmethod
    def change_amount(cls, request, product_id, seller_id,
                      count, user=None, session_products=None):
        """
        Изменить количество товара в корзине
        Если есть словарь с товарами из сессии <session_products>,
        то метод вернёт обновлённый словарь для обновления текущей сессии.
        """
        if user:
            product = rep_prod.get_product_by_id(product_id)  # продукт по id
            seller = rep_seller.get_seller(seller_id)  # продавец по id
            cart = rep_cart.get_cart(user=user)  # корзина пользователя
            cart_item = CartItem.objects.get(cart=cart,
                                             product=product,
                                             seller=seller)
            #  позиция с товаром в корзине
            rep_cart_item.save(force=cart_item, quantity=count)
            # изменение количества товара в корзине
        else:
            if session_products:  # если есть товары в сессии
                session_products[str(product_id)][0] = count
                # изменение количества товара в корзине
                return session_products

    @classmethod
    def move_from_session(cls, user, session_products):
        """
        Добавление товаров в корзину пользователя
        из сессии
        """
        cart = rep_cart.get_cart(user)
        for product_id in session_products:
            # цикл по product_id в сессии
            product = rep_prod.get_product_by_id(product_id)  # товар по id
            seller = rep_seller. \
                get_seller(int(session_products[product_id][1]))
            cart_item = rep_cart_item. \
                get_cart_item(cart=cart, product=product, seller=seller)
            if cart_item:
                # позиция с этим товаром от этого продавца в корзине уже есть
                count = session_products[product_id][0]
                cart_item.update(quantity=F('quantity') + count)
            else:
                rep_cart_item.save(
                    cart=cart,
                    product=product,
                    seller=seller,
                    quantity=session_products[product_id][0]
                )
            # создание позиций в корзине
