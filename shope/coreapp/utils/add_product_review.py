from authapp.models import User
from productsapp.models import Product, Review


class AddProductReview:
    """
    Сервис добавления отзыва к товару
    """

    @classmethod
    def add_product_review(cls,
                           user: User,
                           product: Product,
                           text: str):
        """
        Добавление отзыва к товару

        :param user: объект User, который дает отзыв
        :param product: объект Product, которому адресован отзыв
        :param text: текст отзыва
        :return: str
        """
        if user.is_anonymous:
            return "Чтобы оставить отзыв, " \
                   "вам нужно авторизоваться - http://localhost:8000/signup/"

        Review.objects.create(user=user,
                              product=product,
                              text=text)
        return "Отзыв успешно добавлен"

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
