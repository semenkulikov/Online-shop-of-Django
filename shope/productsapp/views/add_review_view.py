from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from productsapp.models import Product
from productsapp.forms import AddReviewForm
from coreapp.utils.add_product_review import AddProductReview
from repositories.price_repository import PriceRepository
from repositories.profile_repository import ProfileRepository
from repositories import SellerSelectRepository, SpecificSelectRepository


class AddReviewView(View):
    """
    Класс-view для добавления отзыва к продукту
    """
    form_class = AddReviewForm
    _service = AddProductReview()
    _profile_repository = ProfileRepository()
    select_seller_repo = SellerSelectRepository()
    select_specifics_repo = SpecificSelectRepository()
    _price_repository = PriceRepository()

    def get(self, request: HttpRequest, product_id: int) -> HttpResponse:
        product = Product.objects.get(id=product_id)
        product_price = self._price_repository.get_avg_prices(product=product)
        # получаем конкретный продукт
        amount_review = self._service.product_reviews_amount(product=product)
        # количество отзывов
        reviews_list = self._service.product_reviews_list(product=product)[:1]
        # список отзывов
        sellers = self.select_seller_repo.get_seller_by_product(
            product=product
        )
        specifics = self.select_specifics_repo.get_specific_by_product(
            product=product
        )

        return render(request, "productsapp/product.html",
                      context={"form": self.form_class,
                               "product": product,
                               "product_price": product_price,
                               "amount_review": amount_review,
                               "reviews_list": reviews_list,
                               'sellers': sellers,
                               'specifics': specifics,
                               "user": request.user})

    def post(self, request: HttpRequest, product_id: int) -> HttpResponse:
        form = self.form_class(data=request.POST)  # форма с отзывом
        product = Product.objects.get(id=product_id)
        product_price = self._price_repository.get_avg_prices(product=product)
        amount_review = self._service.product_reviews_amount(product=product)
        reviews_list = self._service.product_reviews_list(product=product)
        print(request.POST)
        if "show_more" in request.POST:
            reviews_list = self._service.product_reviews_list(product=product)
        else:
            reviews_list = self._service.product_reviews_list(
                product=product
            )[:1]
        if form.is_valid():
            # Если форма валидна, берем отзыв и добавляем к продукту
            text = form.cleaned_data.get("text")
            result = self._service.add_product_review(
                user=self._profile_repository.get_profile(request.user),
                product=product,
                text=text
            )
        else:
            result = "Введены некорректные данные!"
        return render(request, "productsapp/product.html",
                      context={"form": self.form_class,
                               "product": product,
                               "product_price": product_price,
                               "result": result,
                               "amount_review": amount_review,
                               "reviews_list": reviews_list})
