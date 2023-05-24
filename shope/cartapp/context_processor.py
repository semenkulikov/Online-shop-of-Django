from repositories.cart_repository import RepCart
from repositories.price_repository import PriceRepository
from repositories.product_select_repository import ProductSelectRepository
from repositories.seller_select_repository import SellerSelectRepository

rep_cart = RepCart()
rep_price = PriceRepository()
rep_prod = ProductSelectRepository()
rep_sell = SellerSelectRepository()


def cart_block(request):
    """
    Контекстный процессор для отображения
    количества товаров в корзине и общей цены товаров в корзине
    """
    if request.user.is_authenticated and request.user.is_superuser is not True:
        print('ars')
        # если пользователь авторизован и он не является администратором
        user = request.user
        cart = rep_cart.get_cart(user=user)  # корзина пользователя
        context = {
            'cart_count': rep_cart.count_items(cart),
            'cart_sum': rep_cart.get_total_amount(cart)
        }  # словарь с количеством и суммой товаров в корзине
        return context

        # сюда добавить миниатюру аватарки, если есть. и тоже передать.

    else:
        if request.session.get('products'):  # есть товары в сессии
            cart_sum = sum([rep_price.
                           get_price(product=rep_prod.
                                     get_product_by_id(product_id),
                                     seller=rep_sell.
                                     get_seller(request.
                                                session['products']
                                                [product_id][1]
                                                )
                                     )
                            * request.session['products'][product_id][0]
                            for product_id in request.session['products']])
            #  сумма товаров в корзине,
            #  с помощью цикла берутся product_id, count, seller_id
            #  из сессии
            context = {
                'cart_count': sum([value[0] for value in
                                   request.session['products'].values()]),
                'cart_sum': cart_sum
            }  # словарь с количеством и суммой товаров в корзине
            return context
        else:
            return {
                'cart_count': 0,
                'cart_sum': 0
            }
