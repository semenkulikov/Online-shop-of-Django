from interfaces.discount_select_interface import DiscountInterface
from datetime import datetime
from productsapp.models import CartDiscount, SetDiscount, \
    Product, Category, ProductDiscount
from django.db.models import QuerySet


class DiscountRepository(DiscountInterface):
    """
    Репозиторий для работы со скидками
    """

    def get_discount_by_product_or_category(self, product: Product,
                                            category: Category) -> float:
        """
        Метод получения скидки на товар и/или категорию
        возвращает значение скидки
        """
        date_now = datetime.now()
        product_discount = product.product_discounts.filter(
            start_date__lte=date_now, expiration_date__gte=date_now,
            is_active=True).order_by('-priority'). \
            only('value', 'priority')[:1]
        # наиболее приоритетная скидка на товар, если есть
        category_discount = category.category_discounts.filter(
            start_date__lte=date_now, expiration_date__gte=date_now,
            is_active=True).order_by('-priority'). \
            only('value', 'priority')[:1]
        # наиболее приоритетная скидка на категорию, если есть
        total = (category_discount | product_discount). \
            order_by('-priority').first()
        # наиболее приоритетная скидка среди категорий и товаров
        if total:
            return total
        else:
            return False

    def get_discount_by_cart(self) -> CartDiscount:
        """
        Метод получения скидки на корзину
        возвращает экземпляр CartDiscount
        """
        date_now = datetime.now()
        cart_discount = CartDiscount.objects.filter(
            start_date__lte=date_now, expiration_date__gte=date_now,
            is_active=True).order_by('-priority') \
            .only('required_sum', 'required_quantity',
                  'value', 'priority').first()
        return cart_discount

    def get_set_discounts_for_product(
            self, product: Product) -> QuerySet[SetDiscount]:
        """
        Получить все скидки на наборы, в которых есть данный продукт
        """
        date_now = datetime.now()
        return product.set_discounts.filter(start_date__lte=date_now,
                                            expiration_date__gte=date_now,
                                            is_active=True)

    def get_set_discounts_all(self):
        """
        Получить все скидки на наборы, которые
        действуют сейчас или будет действовать
        в будущем
        """
        date_now = datetime.now()
        set_discounts = SetDiscount.objects.filter(
            expiration_date__gte=date_now, is_active=True
        )
        return set_discounts

    def get_cart_discounts_all(self):
        """
        Получить все скидки на корзину, которые
        действуют сейчас или будет действовать
        в будущем
        """
        date_now = datetime.now()
        cart_discounts = CartDiscount.objects.filter(
            expiration_date__gte=date_now, is_active=True
        )
        return cart_discounts

    def get_products_discounts_all(self):
        """
        Получить все скидки на товары, которые
        действуют сейчас или будет действовать
        в будущем
        """
        date_now = datetime.now()
        products_discounts = ProductDiscount.objects.filter(
            expiration_date__gte=date_now, is_active=True
        ).prefetch_related('products')
        return products_discounts

    def get_product_with_discount(self):
        date_now = datetime.now()
        product_discount = ProductDiscount.objects.filter(
            start_date__lte=date_now, expiration_date__gte=date_now,
            is_active=True)[:1].prefetch_related('products')
        return product_discount
