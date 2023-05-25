from django import template
from repositories.price_repository import PriceRepository

rep_price = PriceRepository()
register = template.Library()


@register.simple_tag()
def get_price(product, seller, quantity):
    """Возвращает цену на товар в корзине
    с учётом его количества"""
    price = rep_price.get_price(product, seller) * quantity
    return price
