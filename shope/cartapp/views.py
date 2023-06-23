from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse

from coreapp.utils import AddToCart, SelectCart, ProductDiscounts
from repositories import DiscountRepository, RepCart

disc_rep = DiscountRepository()
cart_rep = RepCart()


class CartItemListView(View):
    """
    Класс для отображения всех товаров в корзине
    """
    template_name = 'cartapp/cart.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # пользователь авторизован
            cart_items = SelectCart.cart_items_list(user=request.user)
            context = {
                'items': cart_items,
                'session': False
            }
            return render(request, self.template_name, context=context)
        else:  # пользователь не авторизован
            if request.session.get('products', False):  # есть товары в сессии
                items_price = SelectCart. \
                    cart_items_list(session_products=request.
                                    session['products'])
                # все товары в корзине,
                # которые есть в сессии
                count_list = [value for value in
                              request.session['products'].values()]
                session_products = request.session.get('products')
                count = SelectCart.cart_all_products_amount(
                    session_products=session_products)
                cart_price = SelectCart.cart_total_amount(
                    session_products=session_products)
                discounted_prices_list = ProductDiscounts. \
                    get_prices_discount_on_cart(
                        cart_price,
                        count,
                        session_products=session_products
                    )
                request.session['prices'] = discounted_prices_list
                request.session.modified = True
                # список количества для каждого товара
                context = {'items': zip(count_list,
                                        items_price,
                                        discounted_prices_list),
                           'session': True,
                           'count_cart': count,
                           'total_amount': round(sum(discounted_prices_list),
                                                 2
                                                 )
                           }
                return render(request, self.template_name, context)
            else:
                return render(request, self.template_name)


class UpdateCartView(View):
    """
    Общий класс для выполнения операций с товарами
    """
    method_service = AddToCart.add_to_cart

    # метод из сервиса для выполнения нужной операции с корзиной
    # для работы класса-view обязательно указать метод из сервиса
    # в противном случае будет ошибка

    def get(self, request, **kwargs):
        if request.user.is_authenticated:  # пользователь авторизован
            kwargs['user'] = request.user
            self.method_service(**kwargs)
        else:
            kwargs['session_products'] = request.session.get('products')
            # есть товары в сессии
            products = self.method_service(**kwargs)
            request.session['products'] = products
            request.session.modified = True

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddToCartView(UpdateCartView):
    """
    Класс для добавления товара в корзину
    """


class RemoveFromCartView(UpdateCartView):
    """
    Класс для удаления товара из корзины
    """
    method_service = AddToCart.delete_from_cart


class DeleteItemCartView(UpdateCartView):
    """
    Класс для удаления позиции с товаром из корзины
    """
    method_service = AddToCart.delete_from_cart

    def get(self, request, **kwargs):
        kwargs['full'] = True
        super().get(request, **kwargs)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ChangeQuantityCartView(UpdateCartView):
    """
    Класс для изменения количества товара в корзине
    """
    method_service = AddToCart.change_amount


class AjaxUpdateCartView(View):
    method_service = AddToCart.add_to_cart

    def get(self, request, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if request.user.is_authenticated:  # пользователь авторизован
                # обновляем kwargs
                kwargs['user'] = request.user
                kwargs['count'] = request.GET.get('quantity', 1)
                self.method_service(**kwargs)
                cart = cart_rep.get_cart(user=request.user)
                cart_count = SelectCart. \
                    cart_all_products_amount(cart=cart)
                cart_sum = SelectCart. \
                    cart_total_amount(cart=cart)
                discounted_total_price = ProductDiscounts. \
                    get_prices_discount_on_cart(cart_sum,
                                                cart_count,
                                                cart=cart)
            else:

                kwargs['session_products'] = request.session.get('products')
                kwargs['count'] = int(request.GET.get('quantity', 1))
                # есть товары в сессии
                products = self.method_service(**kwargs)
                request.session['products'] = products
                cart_count = SelectCart. \
                    cart_all_products_amount(session_products=products)
                cart_sum = SelectCart. \
                    cart_total_amount(session_products=products)
                discounted_total_price = ProductDiscounts. \
                    get_prices_discount_on_cart(cart_sum, cart_count,
                                                session_products=products)
                request.session['prices'] = discounted_total_price
                request.session.modified = True
            context = {'cart_count': cart_count,
                       'cart_sum': round(sum(discounted_total_price), 2)
                       }
            return JsonResponse(data=context)


class AddToCartAjaxView(AjaxUpdateCartView):
    method_service = AddToCart.add_to_cart


class RemoveFromCartAjaxView(AjaxUpdateCartView):
    method_service = AddToCart.delete_from_cart


class DeleteCartItemAjaxView(AjaxUpdateCartView):
    method_service = AddToCart.delete_from_cart

    def get(self, request, **kwargs):
        kwargs['full'] = True
        print(kwargs)
        super().get(request, **kwargs)


class ChangeQuantityCartAjaxView(AjaxUpdateCartView):
    """
    Класс для изменения количества товара в корзине
    """
    method_service = AddToCart.change_amount
