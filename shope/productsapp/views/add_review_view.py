from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from productsapp.models import Product
from productsapp.forms import AddReviewForm
from coreapp.utils.add_product_review import AddProductReview
from repositories.price_repository import PriceRepository
from repositories.product_select_repository import ProductSelectRepository
from repositories.profile_repository import ProfileRepository
from repositories import SellerSelectRepository, SpecificSelectRepository


class AddReviewView(View):
    """
    Класс-view для добавления отзыва к продукту
    """
    form_class = AddReviewForm
    template_name = "productsapp/product.html"
    _service = AddProductReview()
    _profile_repository = ProfileRepository()
    _product_repository = ProductSelectRepository()
    select_seller_repo = SellerSelectRepository()
    select_specifics_repo = SpecificSelectRepository()
    _price_repository = PriceRepository()

    def get(self, request: HttpRequest, product_id: int) -> HttpResponse:
        product = Product.objects.get(id=product_id)
        product_price = self._price_repository.get_avg_prices(product=product)
        # получаем конкретный продукт
        amount_review = self._service.product_reviews_amount(product=product)
        # количество отзывов
        reviews_list = self._service.product_reviews_list(
            product=product,
            count=1)
        # список отзывов
        sellers = self.select_seller_repo.get_seller_by_product(
            product=product
        )
        specifics = self.select_specifics_repo.get_specific_by_product(
            product=product
        )

        return render(request, self.template_name,
                      context={"form": self.form_class,
                               "product": product,
                               "product_price": product_price,
                               "amount_review": amount_review,
                               "reviews_list": reviews_list,
                               'sellers': sellers,
                               'specifics': specifics,
                               "user": request.user})

    def post(self,
             request: HttpRequest,
             product_id: int) -> HttpResponse:
        form = self.form_class(data=request.POST)  # форма с отзывом
        product = self._product_repository.get_product_by_id(
            product_id=product_id
        )
        product_price = self._price_repository.get_avg_prices(
            product=product
        )
        amount_review = self._service.product_reviews_amount(
            product=product
        )
        reviews_list = self._service.product_reviews_list(
            product=product
        )
        is_show_more = False  # Нажата ли кнопка "Показать еще"
        if "show_more" in request.POST:
            reviews_list = self._service.product_reviews_list(product=product)
            is_show_more = True
        else:
            reviews_list = self._service.product_reviews_list(
                product=product,
                count=1,
            )
        if request.user.is_authenticated:
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
        else:
            result = False
        return render(request, self.template_name,
                      context={"form": self.form_class,
                               "product": product,
                               "product_price": product_price,
                               "result": result,
                               "amount_review": amount_review,
                               "reviews_list": reviews_list,
                               "is_show": is_show_more})
