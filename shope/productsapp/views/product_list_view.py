from django.views.generic import ListView
from productsapp.models.product import Product
from taggit.models import Tag
from productsapp.forms.catalog_filter_form import CatalogFilterForm
from repositories.product_select_repository import ProductSelectRepository


class ProductListView(ListView):
    """ Класс-view для каталога """
    template_name = 'productsapp/catalog.html'
    model = Product
    paginate_by = 8
    extra_context = {'tags_list': Tag.objects.all()}
    queryset = Product.objects.all()
    select_repo = ProductSelectRepository()

    def get_queryset(self):
        form = CatalogFilterForm(self.request.GET)
        if form.is_valid():
            price_min = form.cleaned_data.get('price_min')
            price_max = form.cleaned_data.get('price_max')
            tag = form.cleaned_data.get('tag')
            sort = form.cleaned_data.get('sort')

            if tag:
                queryset = self.select_repo.get_products_with_tag(tag=tag)
            else:
                queryset = self.select_repo.get_products_with_filter(
                    name=form.cleaned_data.get('name'),
                    free_delivery=form.cleaned_data.get('free_delivery'),
                    in_stock=form.cleaned_data.get('in_stock'))
            # получение цен из среза
            queryset = self.select_repo.get_product_prices(queryset)
            # ограничение выборки по цене, если диапазон задан
            if price_min and price_max:
                queryset = queryset.filter(
                    price__range=(price_min, price_max))
            return self.select_repo.get_sorted(products=queryset,
                                               sort=sort)
        else:
            return self.queryset
