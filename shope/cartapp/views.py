from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect

from coreapp.utils.select_cart import SelectCart
from coreapp.utils.update_cart import AddToCart


class CartItemListView(View):
    """
    Класс для отображения всех продуктов в корзине
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
                count_list = [product[0] for product in
                              request.session['products'].values()]
                # список количества для каждого товара
                context = {'items': zip(count_list, items_price),
                           'session': True}
                return render(request, self.template_name, context)
            else:
                return render(request, self.template_name)


class ProductUpdateView(View):
    """
    Общий класс для выполнения операций с товарами
    """
    method_service = AddToCart.add_to_cart
    # метод из сервиса для выполнения нужной операции с корзиной

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


class AddProductCartView(ProductUpdateView):
    """
    Класс для добавления товара в корзину
    """


class RemoveProductCartView(ProductUpdateView):
    """
    Класс для удаления товара из корзины
    """
    method_service = AddToCart.delete_from_cart


class DeleteItemCartView(ProductUpdateView):
    """
    Класс для удаления позиции с товаром из корзины
    """
    method_service = AddToCart.delete_from_cart

    def get(self, request, **kwargs):
        kwargs['full'] = True
        super().get(request, **kwargs)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ChangeQuantityCartView(ProductUpdateView):
    """
    Класс для изменения количества товара в корзине
    """
    method_service = AddToCart.change_amount


class AjaxAddProductView(View):

    method_service = AddToCart.add_to_cart

    def get(self, request, **kwargs):
        if request.is_ajax():
            print('ajx')
