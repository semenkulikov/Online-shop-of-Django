from django.db.models import QuerySet

from interfaces.reviews_interface import ReviewInterface
from productsapp.models import Review, Product


class ReviewRepository(ReviewInterface):

    def get_all_reviews(self, product: Product) -> QuerySet[Review]:
        return product.reviews.all()

    def get_amount_reviews(self, product: Product) -> int:
        return product.reviews.count()

    def save(self, review: Review, force=None) -> None:
        if force:
            review.save(force)
        review.save()
