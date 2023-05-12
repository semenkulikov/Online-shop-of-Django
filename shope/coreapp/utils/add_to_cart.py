from productsapp.models.product import Product
from cartapp.models.cartitem import CartItem

from django.shortcuts import get_object_or_404
from django.db.models import F

from repositories.cart_repository import RepCart, RepCartItem


class AddToCart:
    """
    Сервис добавления товара в корзину
    """

    @classmethod
    def add_to_cart(cls, request, product_id, count=1):
        """
        Добавление товара в корзину
        """
        if request.user.is_authenticated:  # если пользователь авторизован
            product = get_object_or_404(Product, pk=product_id)
            user = request.user
            cart = RepCart().get_cart(user=user)
            cart_item = RepCartItem().get_cart_item(cart=cart, product=product)
            if not cart_item:  # товара нет в корзине
                RepCartItem().save(cart=cart, product=product, quantity=count)

            else:  # товар есть в корзине
                if count != 1:  # изменение количества
                    cls.change_amount(request, product_id, count)
                else:  # увеличение количества на 1
                    cart_item.update(quantity=F('quantity') + 1)
        else:  # если анонимный пользователь
            if request.session.get('products', False) is not False:
                #  если есть в сессиях уже какие-либо товары
                if request.session['products'].\
                        get(str(product_id), False) is not False:
                    # если позиция с конкретным товаром уже есть и count != 1
                    # изменить количество на count
                    if count != 1:
                        request.session['products'][str(product_id)] = count
                    else:
                        # увеличить количество на 1
                        request.session['products'][str(product_id)] += 1
                else:  # товара в корзине нет
                    request.session['products'][str(product_id)] = count
            else:  # в сессии нет товаров
                request.session['products'] = {str(product_id): count}
            request.session.modified = True

    @classmethod
    def delete_from_cart(cls, request, product_id, full=False):
        """
        Удаление товара из корзины
        """
        product = get_object_or_404(Product, pk=product_id)
        if request.user.is_authenticated:  # если пользователь авторизован
            user = request.user
            cart = RepCart().get_cart(user=user)
            cart_item = RepCartItem().get_cart_item(cart=cart, product=product)
            if full is not False:  # удаление товара из корзины
                RepCartItem().delete(cart_item)
            else:  # уменьшение количества товара на 1
                cart_item.update(quantity=F('quantity') - 1)
        pass

    @classmethod
    def change_amount(cls, request, product_id, count=1):
        """
        Изменить количество товара в корзине
        """
        product = get_object_or_404(Product, pk=product_id)
        user = request.user
        cart = RepCart().get_cart(user=user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        RepCartItem().save(force=cart_item, quantity=count)

    @classmethod
    def cart_items_list(cls, cart=None, list_product_id=None):
        """
        Получение списка товаров в корзине
        """
        if list_product_id:
            items_list = [Product.objects.get(pk=product_id)
                          for product_id in list_product_id]
        else:
            items_list = RepCartItem().get_all_items(cart)
        return items_list

    @classmethod
    def cart_items_amount(cls, cart):
        """
        Получение общего количества товаров в корзине
        """
        count = RepCart().count_items(cart)
        return count

    @classmethod
    def move_from_session(cls, request, user):
        """
        Добавление товаров в корзину пользователя
        из сессии
        """

        cart = RepCart().get_cart(user)
        for product_id in request.session['products']:
            # цикл по product_id в сессии
            product = get_object_or_404(Product, pk=product_id)
            cart_item = RepCartItem().\
                get_cart_item(cart=cart, product=product)
            if cart_item:
                cart_item.\
                    update(quanity=F('quantity') + request.
                           session['products'][product_id])
            else:
                RepCartItem().save(
                    cart=cart,
                    product=product,
                    quantity=request.session['products'][product_id]
                )
            # создание позиций в корзине
