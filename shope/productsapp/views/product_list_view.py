from django.views.generic import ListView

from productsapp.models import Product


class ProductListView(ListView):
    """ Класс-view для каталога """
    model = Product
    template_name = "productsapp/catalog.html"
    context_object_name = "products"
