from interfaces.reviews_update_interface import ReviewUpdateInterface
from productsapp.models import Review


class ReviewUpdateRepository(ReviewUpdateInterface):
    def update_review(self, review: Review, force=None) -> None:
        if force:
            review.save(force)
        review.save()
