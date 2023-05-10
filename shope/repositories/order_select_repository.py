from django.db.models import QuerySet
from interfaces import OrderInterface
from orderapp.models import Order
from authapp.models import User


class OrderRepository(OrderInterface):

    def get_all(self) -> QuerySet[Order]:
        return Order.objects.all()

    def get_last_activ(self, user: User) -> QuerySet[Order]:
        return Order.objects.filter(
            user=user,
            is_active=True,
            ).order_by('created_at').last()
