def cart_block(request):
    """
    Context-processor for cart block in header.
    """
    if request.user.is_authenticated:
        return {
            'cart': request.user.cart.filter(
                is_active=True
            ).order_by('created_at').first(),
            # сюда добавить миниатюру аватарки, если есть. и тоже передать.
        }
    # переписать, когда будут сделаны сессии
    return {
        'cart': None,
    }
