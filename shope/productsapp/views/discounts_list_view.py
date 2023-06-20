from itertools import chain
from django.views.generic import View
from django.shortcuts import render
from django.db.models import Value
from repositories.discount_select_repository import DiscountRepository
from django.core.paginator import Paginator
from datetime import datetime

rep_discount = DiscountRepository()


class DiscountsListView(View):
    template_name = 'productsapp/sale.html'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        set_discounts = rep_discount.get_set_discounts_all()
        # все скидки на наборы товаров
        cart_discounts = rep_discount.get_cart_discounts_all()
        # все скидки на корзину
        products_discounts = rep_discount.get_products_discounts_all()
        # все скидки на товары
        products = [discount.products.filter(is_active=True).annotate(
            value=Value(discount.value),
            type=Value('product'),
            start_date=Value(datetime.strftime(discount.start_date,
                                               '%b-%d-%Y')),
            expiration_date=Value(
                datetime.strftime(discount.expiration_date, '%b-%d-%Y')) if
            discount.expiration_date else Value('')
        ) for discount in
            products_discounts]
        # все товары, у которых есть скидка
        categories = [discount.categories.filter(is_active=True).annotate(
            value=Value(discount.value),
            type=Value('category'),
            start_date=Value(datetime.strftime(discount.start_date,
                                               '%b-%d-%Y')),
            expiration_date=Value(
                datetime.strftime(discount.expiration_date, '%b-%d-%Y')) if
            discount.expiration_date else Value('')
        ) for discount in
            products_discounts]
        # все категории, у которых есть скидка
        result_list = list(chain(cart_discounts,
                                 set_discounts,
                                 *categories,
                                 *products))
        # общий список всех скидок на товары, корзины, наборы товаров
        paginator = Paginator(result_list, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj
        }
        return render(request, self.template_name, context)
