from interfaces.product_select_interface import ProductSelectInterface
from productsapp.models.product import Product
from productsapp.models.specific import Specific
from django.db.models import QuerySet, Min, Sum, Count, Subquery, OuterRef


class ProductSelectRepository(ProductSelectInterface):

    def get_all_products(self) -> QuerySet[Product]:
        """Получить все продукты"""
        return Product.objects.all()

    def get_products_with_filter(self,
                                 name: str,
                                 free_delivery: bool,
                                 in_stock: bool) -> QuerySet[Product]:
        """Получить список продуктов на основании фильтра"""
        return Product.objects.filter(
            name__icontains=name,
            free_delivery__in=(True, free_delivery),
            is_active__in=(True, in_stock))

    def get_products_with_tag(self,
                              tag: str) -> QuerySet[Product]:
        """Получить список продуктов по тегу"""
        return Product.objects.filter(tags__name__in=[tag])

    def get_product_prices(self,
                           products: QuerySet) -> QuerySet[Product]:
        """Получить цены на список продуктов"""
        prices = products.select_related('category').annotate(
            price=Min('product_price__value'))
        return prices

    def sort_by_popular(self,
                        products: QuerySet,
                        reverse: bool) -> QuerySet[Product]:
        """ Cортировка по количеству проданных """
        prefix = ''
        if reverse:
            prefix = '-'
        sorted_products = products.annotate(
            sold=Sum('ordered__count')).order_by(f'{prefix}sold')
        return sorted_products

    def sort_by_reviews(self,
                        products: QuerySet,
                        reverse: bool) -> QuerySet[Product]:
        """ Cортировка по количеству отзывов """
        prefix = ''
        if reverse:
            prefix = '-'
        sorted_products = products.annotate(
            reviews_amount=Count('review')).order_by(
            f'{prefix}reviews_amount')
        return sorted_products

    def sort_by_new(self,
                    products: QuerySet,
                    reverse: bool) -> QuerySet[Product]:
        """ Cортировка по году выпуска """
        prefix = ''
        if reverse:
            prefix = '-'
        sorted_products = products.annotate(
            year=Subquery(
                Specific.objects.filter(
                    type_spec__name='Год выпуска',
                    product=OuterRef('pk')
                ).values('description'))).order_by(f'{prefix}year')
        return sorted_products

    def sort_by_price(self,
                      products: QuerySet,
                      reverse: bool) -> QuerySet[Product]:
        """ Cортировка по цене """
        prefix = ''
        if reverse:
            prefix = '-'
        return products.order_by(f'{prefix}price')
