from django.views import View
from django.shortcuts import render
from coreapp.utils.add_to_cart import AddToCart
from django.http import HttpResponseRedirect
from repositories.cart_repository import RepCart


class CartItemListView(View):
    """
    Класс для отображения всех продуктов в корзине
    """
    template_name = 'cartapp/cart.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # пользователь авторизован
            cart = RepCart().get_cart(user=request.user)
            cart_items = AddToCart.cart_items_list(cart=cart)
            #  все товары в корзине

            context = {'items': cart_items}
            return render(request, self.template_name, context)
        else:  # пользователь не авторизован
            if request.session.get('products', False):  # есть товары в сессии
                list_product_id = [product_id for product_id in
                                   request.session['products'].keys()]
                products = AddToCart. \
                    cart_items_list(list_product_id=list_product_id)
                # все товары в корзине,
                # которые есть в сессии
                count_list = [product_quantity for product_quantity in
                              request.session['products'].values()]
                # список количества для каждого товара
                context = {'items': products,
                           'count_list': count_list}
                return render(request, self.template_name, context)
            else:
                return render(request, self.template_name)

    def post(self, request):
        pass


class AddProductCartView(View):
    """
    Класс для добавления продукта в корзину
    """

    def get(self, request, **kwargs):
        product_id = kwargs.get('product_id')
        AddToCart.add_to_cart(request, product_id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RemoveProductCartView(View):
    """
    Класс для удаления товара из корзины
    """

    def get(self, request, **kwargs):
        product_id = kwargs.get('product_id')
        AddToCart.delete_from_cart(request, product_id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteItemCartView(View):
    """
    Класс для удаления позиции с товаром
    """

    def get(self, request, **kwargs):
        product_id = kwargs.get('product_id')
        AddToCart.delete_from_cart(request, product_id, full=True)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
