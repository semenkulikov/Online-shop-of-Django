from itertools import chain
from django.views.generic import View
from django.shortcuts import render
from django.db.models import Value, QuerySet
from repositories.discount_select_repository import DiscountRepository
from django.core.paginator import Paginator
from datetime import datetime
from productsapp.models import ProductDiscount, Product, Category
from typing import Tuple, List
from django.http import HttpRequest, HttpResponse

rep_discount = DiscountRepository()


class DiscountsListView(View):
    """
    Класс для отображения всех скидок
    """
    template_name = 'productsapp/sale.html'
    paginate_by = 12

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        set_discounts = rep_discount.get_set_discounts_all()
        cart_discounts = rep_discount.get_cart_discounts_all()
        products_discounts = rep_discount.get_products_discounts_all()
        products, categories = get_object_discounts_list(products_discounts)
        result_list = list(chain(cart_discounts, set_discounts,
                                 *categories, *products))
        # общий список всех скидок на товары, корзины, наборы товаров
        paginator = Paginator(result_list, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return render(request, self.template_name, context)


def get_object_discounts_list(discount_queryset: QuerySet[ProductDiscount]) \
        -> Tuple[List[Product], List[Category]]:
    """
    Метод, который возвращает список всех товаров
    и категорий со скидкой с аннотацией по датам
    действия скидки
    """

    products = [discount.products.filter(is_active=True).annotate(
        value=Value(discount.value), type=Value('product'),
        start_date=Value(datetime.strftime(discount.start_date,
                                           '%b-%d-%Y')),
        expiration_date=Value(
            datetime.strftime(discount.expiration_date, '%b-%d-%Y')) if
        discount.expiration_date else Value('')
    ) for discount in
        discount_queryset]  # все товары, у которых есть скидка
    categories = [discount.categories.filter(is_active=True).annotate(
        value=Value(discount.value), type=Value('category'),
        start_date=Value(datetime.strftime(discount.start_date,
                                           '%b-%d-%Y')),
        expiration_date=Value(
            datetime.strftime(discount.expiration_date, '%b-%d-%Y')) if
        discount.expiration_date else Value('')
    ) for discount in
        discount_queryset]
    return products, categories
