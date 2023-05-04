from productsapp.models import Product, Review
from profileapp.models import Profile


class AddProductReview:
    """
    Сервис добавления отзыва к товару
    """

    @classmethod
    def add_product_review(cls,
                           user: Profile,
                           product: Product,
                           text: str):
        """
        Добавление отзыва к товару

        :param user: объект User, который дает отзыв
        :param product: объект Product, которому адресован отзыв
        :param text: текст отзыва
        :return: bool
        """
        if user.user.is_anonymous:
            return False

        Review.objects.create(user=user,
                              product=product,
                              text=text)
        return True

    @classmethod
    def product_reviews_list(cls, product: Product):
        """
        Получение списка отзывов к товару

        :param product: объект Product, у которого берем отзывы
        :return: QuerySet
        """
        return product.review.all()

    @classmethod
    def product_reviews_amount(cls, product: Product):
        """
        Получение количества отзывов для товара

        :param product: объект Product, у которого находим кол-во отзывов.

        :return: int
        """

        return product.review.count()
