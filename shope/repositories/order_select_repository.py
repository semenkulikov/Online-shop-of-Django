from interfaces import OrderInterface
from orderapp.models import Order
from authapp.models import User
from django.db.models import QuerySet, Sum


class OrderRepository(OrderInterface):

    def get_all(self) -> QuerySet[Order]:
        return Order.objects.annotate(
            sum_price=Sum('order_items__price'),
        )

    def get_last_activ(self, user: User) -> QuerySet[Order]:
        return Order.objects.annotate(
            sum_price=Sum('order_items__price')
        ).filter(
            user=user,
            is_active=True,
            ).order_by('created_at').last()

    def get_order_by_id(self, order_id: int):
        return Order.objects.annotate(
            amount=Sum('order_items__price')
        ).get(id=order_id)
