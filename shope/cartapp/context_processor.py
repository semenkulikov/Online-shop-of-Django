from repositories.cart_repository import RepCart

rep_cart = RepCart()


def cart_block(request):
    """
    Контекстный процессор для передачи
    количества товаров в корзине
    """
    if request.user.is_authenticated and request.user.is_superuser is not True:
        # если пользователь авторизован и он не является администратором
        user = request.user
        cart = rep_cart.get_cart(user=user)  # корзина пользователя
        context = {
            'cart': rep_cart.count_items(cart=cart),
        }  # словарь с количеством товаров в корзине
        return context

        # сюда добавить миниатюру аватарки, если есть. и тоже передать.

    else:
        if request.session.get('products'):
            context = {
                'cart': sum([value[0] for value in
                             request.session['products'].values()])
            }
            return context
        else:
            return {
                'cart': 0
            }
