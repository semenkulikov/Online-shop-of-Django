from django import template
from repositories import PriceRepository

register = template.Library()
price_rep = PriceRepository()


@register.simple_tag()
def get_price_a_seller(product, seller):
    """Возвращает цену,
    установленную продавцом на товар
    """
    return price_rep.get_price(product, seller)
