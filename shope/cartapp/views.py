from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from coreapp.utils import AddToCart, SelectCart, ProductDiscounts
from repositories import DiscountRepository, RepCart
from .forms import InputAmountForm

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
                discounted_prices_list, discount = ProductDiscounts. \
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
                                                 ),
                           'discount': discount,
                           }
                return render(request, self.template_name, context)
            else:
                return render(request, self.template_name)


class AjaxUpdateCartView(View):
    method_service = AddToCart.add_to_cart
    full_delete = False  # флаг для удаления всей позиции с товаром

    def post(self, request, **kwargs):
        form = InputAmountForm(request.POST)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid():  # передано валидное значение count
                cleaned_data = {key: val for key, val in
                                form.cleaned_data.items() if val is not None}
                if self.full_delete:
                    cleaned_data['full'] = True
                # словарь с полями из формы без нулевых значений
                if request.user.is_authenticated:  # пользователь авторизован
                    self.method_service(**cleaned_data, user=request.user)
                    cart = cart_rep.get_cart(user=request.user)  # корзина
                    cart_count = SelectCart. \
                        cart_all_products_amount(cart=cart)  # количество
                    cart_sum = SelectCart. \
                        cart_total_amount(cart=cart)  # сумма без учета скидки
                    discounted_total_price, discount = ProductDiscounts. \
                        get_prices_discount_on_cart(cart_sum,
                                                    cart_count,
                                                    cart=cart)
                    cart_items = SelectCart.cart_items_list(user=request.user)
                    cart_items_html = render_to_string(
                        'cartapp/cart_ajax.html',
                        context={'items': cart_items,
                                 'cart_sum': round(sum(discounted_total_price),
                                                   2
                                                   ),
                                 'discount': discount,
                                 }

                    )

                    context = {'cart_count': cart_count,
                               'items': cart_items_html,
                               'cart_sum': round(sum(discounted_total_price),
                                                 2
                                                 ),
                               }

                    return JsonResponse(data=context, safe=False)
                else:
                    session_products = request.session.get(
                        'products'
                    )
                    # есть товары в сессии
                    products = self.\
                        method_service(**cleaned_data, session_products=session_products)  # noqa
                    request.session['products'] = products
                    items_list = SelectCart. \
                        cart_items_list(session_products=products)

                    count_list = [value for value in products.values()]
                    # список с количеством товаров
                    total_count = sum(count_list)  # общее количество
                    cart_price = SelectCart.cart_total_amount(
                        session_products=products)  # общая цена без скидки
                    discounted_prices_list, discount = ProductDiscounts. \
                        get_prices_discount_on_cart(
                            cart_price,
                            total_count,
                            session_products=products
                        )
                    request.session['prices'] = discounted_prices_list
                    # обновление сессий новым списком цен со скидками
                    request.session.modified = True
                    cart_items_html = render_to_string(
                        'cartapp/cart_ajax.html',
                        context={
                            'items': zip(
                                count_list,
                                items_list,
                                discounted_prices_list
                            ),
                            'session': True,
                            'cart_sum': round(sum(discounted_prices_list),
                                              2
                                              ),
                            'discount': discount
                        }
                    )
                    context = {'items': cart_items_html,
                               'cart_count': total_count,
                               'cart_sum': round(sum(discounted_prices_list),
                                                 2
                                                 ),
                               }

                    return JsonResponse(data=context, safe=False)


class AddToCartAjaxView(AjaxUpdateCartView):
    method_service = AddToCart.add_to_cart


class ReduceFromCartAjaxView(AjaxUpdateCartView):
    method_service = AddToCart.delete_from_cart


class DeleteCartItemAjaxView(AjaxUpdateCartView):
    method_service = AddToCart.delete_from_cart
    full_delete = True


class ChangeQuantityCartAjaxView(AjaxUpdateCartView):
    """
    Класс для изменения количества товара в корзине
    """
    method_service = AddToCart.change_amount
