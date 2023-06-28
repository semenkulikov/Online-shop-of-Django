from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from repositories import SellerSelectRepository, ProductSelectRepository, PriceRepository

_seller_repository = SellerSelectRepository()
_product_repository = ProductSelectRepository()
_price_repository = PriceRepository()


def seller_detail_view(request: HttpRequest, seller_id: int) -> HttpResponse:
    """ Представление для детальной страницы продавца """
    seller = _seller_repository.get_seller(seller_id=seller_id)
    products = _product_repository.get_products_by_seller_id(seller_id=seller_id)
    for product in products:
        product.price = _price_repository.get_object_price(product, seller).value

    return render(request, "productsapp/detailed_seller.html", {"seller": seller,
                                                                "products": products})
