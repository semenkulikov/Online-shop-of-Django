from repositories.cart_repository import RepCart


def cart_block(request):
    """
    Контекстный процессор для передачи
    количества товаров в корзине
    """
    if request.user.is_authenticated and request.user.is_superuser is not True:
        user = request.user
        cart = RepCart.get_cart(user=user)
        context = {
            'cart': RepCart.count_items(cart=cart),
        }
        return context

        # сюда добавить миниатюру аватарки, если есть. и тоже передать.

    else:
        if request.session.get('products', False):
            context = {
                'cart': sum([value for value in
                             request.session['products'].values()])
            }
            return context
        else:
            return {
                'cart': 0
            }
