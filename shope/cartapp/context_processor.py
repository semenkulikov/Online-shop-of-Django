def cart_block(request):
    """
    Context-processor for cart block in header.
    """
    if request.user.is_authenticated:
        return {
            'cart': request.user.cart.get(is_active=True),
            # сюда добавить миниатюру аватарки, если есть. и тоже передать.
        }
    # переписать, когда будут сделаны сессии
    return {
        'cart_amount': 0,
        'quantity_cart_items': 0
    }
