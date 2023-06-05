from repositories.cart_repository import RepCart
from repositories.price_repository import PriceRepository
from repositories.product_select_repository import ProductSelectRepository
from repositories.seller_select_repository import SellerSelectRepository
from coreapp.utils.select_cart import SelectCart

rep_cart = RepCart()
rep_price = PriceRepository()
rep_prod = ProductSelectRepository()
rep_sell = SellerSelectRepository()


def cart_block(request):
    """
    Контекстный процессор для отображения
    количества товаров в корзине и общей цены товаров в корзине
    """
    if request.user.is_authenticated:
        # если пользователь авторизован и он не является администратором
        user = request.user
        context = {
            'cart_count': SelectCart.cart_items_amount(user=user),
            'cart_sum': SelectCart.cart_total_amount(user=user)
        }  # словарь с количеством и суммой товаров в корзине
        return context

        # сюда добавить миниатюру аватарки, если есть. и тоже передать.

    else:
        session_products = request.session.get('products')
        context = {
            'cart_count': SelectCart.
            cart_items_amount(session_products=session_products),
            'cart_sum': SelectCart.
            cart_total_amount(session_products=session_products)
        }  # словарь с количеством и суммой товаров в корзине
        return context
