from coreapp.models import BaseModel
from django.db import models
from authapp.models import User
from coreapp.enums import PAYMENT_STATUSES


class Payment(BaseModel):
    """
    Класс-модель платежа
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user')
    payment_id = models.CharField(
        max_length=100,
        verbose_name='yookassa payment id')
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='amount')
    status = models.CharField(
        max_length=20,
        verbose_name='payment status',
        choices=PAYMENT_STATUSES)

    def __str__(self):
        return self.payment_id

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'payments'


class Card(BaseModel):
    """
    Класс-модель платежной карты
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user')
    number = models.CharField(
        max_length=20,
        verbose_name='card number')
    payment_method_id = models.CharField(
        max_length=100,
        verbose_name='payment method id')
    card_type = models.CharField(
        max_length=10,
        verbose_name='card type')
    expiration_date = models.DateField(
        verbose_name='expiration date')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'card'
        verbose_name_plural = 'cards'
