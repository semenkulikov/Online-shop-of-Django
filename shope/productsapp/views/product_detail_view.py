from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from productsapp.models import Product
from productsapp.forms import AddReviewForm
from coreapp.utils.add_product_review import AddProductReview
from repositories import SellerSelectRepository, SpecificSelectRepository


class ProductDetailView(View):
    """
    Класс-view для отображения детальной страницы продукта
    """
    form_class = AddReviewForm
    service = AddProductReview()
    select_seller_repo = SellerSelectRepository()
    select_specifics_repo = SpecificSelectRepository()

    def get(self, request: HttpRequest, product_id: int) -> HttpResponse:
        product = Product.objects.get(id=product_id)
        # получаем конкретный продукт
        amount_review = self.service.product_reviews_amount(product=product)
        # количество отзывов
        reviews_list = self.service.product_reviews_list(product=product)
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
                               "amount_review": amount_review,
                               "reviews_list": reviews_list,
                               'sellers': sellers,
                               'specifics': specifics})

    def post(self, request: HttpRequest, product_id: int) -> HttpResponse:
        form = self.form_class(data=request.POST)  # форма с отзывом
        product = Product.objects.get(id=product_id)
        amount_review = self.service.product_reviews_amount(product=product)
        reviews_list = self.service.product_reviews_list(product=product)
        if form.is_valid():
            # Если форма валидна, берем отзыв и добавляем к продукту
            text = form.cleaned_data.get("text")
            result = self.service.add_product_review(
                user=self.request.user,
                product=product,
                text=text
            )
        else:
            result = "Введены некорректные данные!"
        return render(request, "productsapp/product.html",
                      context={"form": self.form_class,
                               "product": product,
                               "result": result,
                               "amount_review": amount_review,
                               "reviews_list": reviews_list})