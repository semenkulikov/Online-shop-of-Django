from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from coreapp.utils.products_comparison_list import ProductsComparisonList
from productsapp.forms import AddReviewForm
from productsapp.models import Product
from coreapp.utils import ViewedProductsService
from coreapp.utils.add_product_review import AddProductReview
from repositories.price_repository import PriceRepository
from repositories.product_image_repository import ProductImageRepository
from repositories.profile_repository import ProfileRepository
from repositories import SellerSelectRepository, SpecificSelectRepository

_profile_repository = ProfileRepository()
_select_seller_repo = SellerSelectRepository()
_select_specifics_repo = SpecificSelectRepository()
_price_repository = PriceRepository()
_product_image_repo = ProductImageRepository()


class ProductDetailView(View):
    """
    Класс-view для отображения детальной страницы продукта
    """
    _service = AddProductReview()
    _comparison_service = ProductsComparisonList()
    _viewed_service = ViewedProductsService()

    template_name = "productsapp/product.html"
    form_class = AddReviewForm

    def get(self, request: HttpRequest, product_id: int) -> HttpResponse:
        product = Product.objects.get(id=product_id)
        # получаем конкретный продукт
        product_price = _price_repository. \
            get_min_price_object(product=product)
        amount_review = self._service.product_reviews_amount(product=product)
        # количество отзывов
        reviews_list = self._service.product_reviews_list(
            product=product,
            count=1)
        # список отзывов
        sellers = _select_seller_repo.get_seller_by_product(
            product=product
        )
        specifics = _select_specifics_repo.get_specific_by_product(
            product=product
        )
        if request.user.is_authenticated:
            self._viewed_service.add_to_viewed_products(
                user=request.user,
                product=product
            )

        self._comparison_service.add_to_comparison(
            request=request,
            product_id=product.pk
        )

        product_images = _product_image_repo.get_all_images(product=product)

        return render(request, self.template_name,
                      context={"product": product,
                               "product_images": product_images,
                               "form": self.form_class,
                               "product_price": product_price,
                               "amount_review": amount_review,
                               "reviews_list": reviews_list,
                               'sellers': sellers,
                               'specifics': specifics,
                               "user": request.user})

    def post(self, request: HttpRequest, product_id: int) -> HttpResponse:
        product = Product.objects.get(id=product_id)
        product_images = _product_image_repo.get_all_images(product=product)
        product_price = _price_repository. \
            get_min_price_object(product=product)
        amount_review = self._service.product_reviews_amount(product=product)
        reviews_list = self._service.product_reviews_list(product=product)
        return render(request, self.template_name,
                      context={"product": product,
                               "product_images": product_images,
                               "product_price": product_price,
                               "amount_review": amount_review,
                               "reviews_list": reviews_list})
