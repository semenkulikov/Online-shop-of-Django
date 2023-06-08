from interfaces import OrderInterface
from orderapp.models import Order
from authapp.models import User
from django.db.models import QuerySet, Sum, Count, Q
from django.conf import settings


class OrderRepository(OrderInterface):

    def get_all(self) -> QuerySet[Order]:
        return Order.objects.annotate(
            sum_price=Sum('order_items__price',
                          filter=Q(order_items__is_active=True)),
        )

    def get_last_activ(self, user: User) -> QuerySet[Order]:
        return Order.objects.annotate(
            sum_price=Sum('order_items__price',
                          filter=Q(order_items__is_active=True))
        ).filter(
            user=user,
            is_active=True,
            ).order_by('created_at').last()

    def get_order_by_id(self, order_id: int):

        order = Order.objects.annotate(
            amount=Sum('order_items__price',
                       filter=Q(order_items__is_active=True)),
            sellers=Count('order_items__seller',
                          distinct=True,
                          filter=Q(order_items__is_active=True))
        ).get(id=order_id)

        # Доставка бесплатна, если все товары от одного
        # продавца и сумма заказа больше заданной.
        order.delivery_price = settings.DELIVERY_PRICE
        if order.amount > settings.FREE_DELIVERY_SUM and order.sellers == 1:
            order.delivery_price = 0

        return order
