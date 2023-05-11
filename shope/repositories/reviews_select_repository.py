from django.db.models import QuerySet

from interfaces.reviews_select_interface import ReviewSelectInterface
from productsapp.models import Review, Product


class ReviewSelectRepository(ReviewSelectInterface):

    def get_all_reviews(self, product: Product) -> QuerySet[Review]:
        return product.review.all()

    def get_amount_reviews(self, product: Product) -> int:
        return product.review.count()
