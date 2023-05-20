from productsapp.models.product import Product
from cartapp.models.cartitem import CartItem

from django.shortcuts import get_object_or_404
from django.db.models import F

from repositories.cart_repository import RepCart, RepCartItem

rep_cart = RepCart()
rep_cart_item = RepCartItem()


class AddToCart:
    """
    Сервис добавления товара в корзину
    """

    @classmethod
    def add_to_cart(cls, request, product_id, count=1, change=False):
        """
        Добавление товара в корзину
        """
        if request.user.is_authenticated:  # если пользователь авторизован
            product = get_object_or_404(Product, pk=product_id)
            user = request.user
            cart = rep_cart.get_cart(user=user)
            cart_item = rep_cart_item.get_cart_item(cart=cart, product=product)
            if not cart_item:  # товара нет в корзине
                rep_cart_item.save(cart=cart, product=product, quantity=count)

            else:  # товар есть в корзине
                if change:  # изменение количества товаров
                    cls.change_amount(request, product_id, count)
                else:  # добавление товаров
                    cart_item.update(quantity=F('quantity') + count)
        else:  # если анонимный пользователь
            if request.session.get('products'):
                #  если есть в сессиях уже какие-либо товары
                if request.session['products']. \
                        get(str(product_id)):
                    # если позиция с конкретным товаром уже есть и change=True
                    if change:
                        request.session['products'][str(product_id)] = count
                        # изменить количество на count
                    else:
                        # увеличить количество на 1
                        request.session['products'][str(product_id)] += 1
                else:  # товара в корзине нет
                    request.session['products'][str(product_id)] = count
            else:  # в сессии нет товаров
                request.session['products'] = {str(product_id): count}
            request.session.modified = True

    @classmethod
    def delete_from_cart(cls, request, product_id, full=None):
        """
        Удаление товара из корзины
        """
        product = get_object_or_404(Product, pk=product_id)
        if request.user.is_authenticated:  # если пользователь авторизован
            user = request.user
            cart = rep_cart.get_cart(user=user)
            cart_item = rep_cart_item.get_cart_item(cart=cart, product=product)
            if full:  # удаление товара из корзины
                rep_cart_item.delete(cart_item)
            else:  # уменьшение количества товара на 1
                cart_item.update(quantity=F('quantity') - 1)
        else:
            if request.session.get('products'):
                if full:  # удаление товара из корзины
                    request.session['products'].pop(str(product_id), False)
                else:  # уменьшение количества на 1
                    request.session['products'][str(product_id)] -= 1
                request.session.modified = True

    @classmethod
    def change_amount(cls, request, product_id, count=1):
        """
        Изменить количество товара в корзине
        """
        product = get_object_or_404(Product, pk=product_id)
        user = request.user
        cart = rep_cart.get_cart(user=user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        rep_cart_item.save(force=cart_item, quantity=count)

    @classmethod
    def cart_items_list(cls, cart=None, list_product_id=None):
        """
        Получение списка товаров в корзине
        """
        if list_product_id:
            items_list = [Product.objects.get(pk=product_id)
                          for product_id in list_product_id]
        else:
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
            cart_item = rep_cart_item. \
                get_cart_item(cart=cart, product=product)
            if cart_item:
                cart_item. \
                    update(quantity=F('quantity') + request.
                           session['products'][product_id])
            else:
                rep_cart_item.save(
                    cart=cart,
                    product=product,
                    quantity=request.session['products'][product_id]
                )
            # создание позиций в корзине
