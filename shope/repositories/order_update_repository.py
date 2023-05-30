from interfaces.order_update_interface import OrderUpdateInterface
from authapp.models import User
from orderapp.models import Order
from coreapp.enums import NOT_PAID_STATUS


class OrderUpdateRepository(OrderUpdateInterface):

    def create(self, user: User):
        """Создать новый заказ"""
        return Order.objects.create(user=user, status=NOT_PAID_STATUS)
