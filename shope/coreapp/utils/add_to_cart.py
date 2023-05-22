from productsapp.models.product import Product
from cartapp.models.cartitem import CartItem

from django.shortcuts import get_object_or_404
from django.db.models import F

from repositories.cart_repository import RepCart, RepCartItem
from repositories.seller_select_repository import SellerSelectRepository

rep_cart = RepCart()
rep_cart_item = RepCartItem()
rep_seller = SellerSelectRepository()


class AddToCart:
    """
    Сервис добавления товара в корзину
    """

    @classmethod
    def add_to_cart(cls, request, product_id, seller_id, count=1):
        """
        Добавление товара в корзину
        """
        if request.user.is_authenticated:  # если пользователь авторизован
            product = get_object_or_404(Product, pk=product_id)
            user = request.user
            cart = rep_cart.get_cart(user=user)
            seller = rep_seller.get_seller(seller_id)
            cart_item = rep_cart_item.get_cart_item(cart=cart,
                                                    product=product,
                                                    seller=seller)
            if not cart_item:  # товара нет в корзине
                rep_cart_item.save(cart=cart, product=product,
                                   seller=seller, quantity=count)
                # создание позиции с товаром
            else:  # товар есть в корзине
                cart_item.update(quantity=F('quantity') + count)
                # добавление товаров
        else:  # анонимный пользователь
            if request.session.get('products'):
                # в сессии есть уже какие-либо товары
                if request.session['products']. \
                        get(str(product_id)):
                    # позиция с товаром уже есть
                    request.session['products'][str(product_id)][0] += count
                    # увеличить количество на count
                else:  # позиция с товаром отсутствует
                    request.session['products'][str(product_id)] = \
                        [count, seller_id]
            else:  # в сессии нет товаров
                request.session['products'] = \
                    {str(product_id): [count, seller_id]}
            request.session.modified = True

    @classmethod
    def delete_from_cart(cls, request, product_id, seller_id, full=None):
        """
        Удаление товара из корзины
        """
        product = get_object_or_404(Product, pk=product_id)
        seller = rep_seller.get_seller(seller_id)
        if request.user.is_authenticated:  # если пользователь авторизован
            user = request.user
            cart = rep_cart.get_cart(user=user)
            cart_item = rep_cart_item.\
                get_cart_item(cart=cart, product=product, seller=seller)
            if full:  # удаление товара из корзины
                rep_cart_item.delete(cart_item)
            else:  # уменьшение количества товара на 1
                cart_item.update(quantity=F('quantity') - 1)
        else:
            if request.session.get('products'):
                if full:  # удаление товара из корзины
                    request.session['products'].pop(str(product_id), False)
                else:  # уменьшение количества на 1
                    request.session['products'][str(product_id)][0] -= 1
                request.session.modified = True

    @classmethod
    def change_amount(cls, request, product_id, seller_id, count):
        """
        Изменить количество товара в корзине
        """
        if request.user.is_authenticated:
            product = get_object_or_404(Product, pk=product_id)
            seller = rep_seller.get_seller(seller_id)
            user = request.user
            cart = rep_cart.get_cart(user=user)
            cart_item = CartItem.objects.get(cart=cart,
                                             product=product,
                                             seller=seller)
            rep_cart_item.save(force=cart_item, quantity=count)
        else:
            if request.session.get('products'):
                request.session['products'][str(product_id)][0] = count

    @classmethod
    def cart_items_list(cls, cart=None, list_product_id=None):
        """
        Получение списка товаров в корзине
        """
        if list_product_id:  # есть товары в сессии
            items_list = [Product.objects.get(pk=product_id)
                          for product_id in list_product_id]
        else:  # товары в сессии отсутствуют
            items_list = rep_cart_item.get_all_items(cart)
        return items_list

    @classmethod
    def cart_items_amount(cls, cart):
        """
        Получение общего количества товаров в корзине
        """
        count = rep_cart.count_items(cart)
        return count

    @classmethod
    def move_from_session(cls, request, user):
        """
        Добавление товаров в корзину пользователя
        из сессии
        """

        cart = rep_cart.get_cart(user)
        for product_id in request.session['products']:
            # цикл по product_id в сессии
            product = get_object_or_404(Product, pk=product_id)
            seller = rep_seller.\
                get_seller(int(request.session['products'][product_id][1]))
            cart_item = rep_cart_item. \
                get_cart_item(cart=cart, product=product, seller=seller)
            if cart_item:
                cart_item. \
                    update(quantity=F('quantity') + request.
                           session['products'][product_id][0])
            else:
                rep_cart_item.save(
                    cart=cart,
                    product=product,
                    seller=seller,
                    quantity=request.session['products'][product_id][0]
                )
            # создание позиций в корзине
