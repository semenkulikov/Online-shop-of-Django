# Статусы платежа
PENDING_STATUS = 'pending'
WAITING_FOR_CAPTURE_STATUS = 'waiting for capture'
CANCELED_STATUS = 'canceled'
SUCCEDED_STATUS = 'succeeded'

PAYMENT_STATUSES = (
    (PENDING_STATUS, 'Создан'),
    (WAITING_FOR_CAPTURE_STATUS, 'Ожидание списания'),
    (CANCELED_STATUS, 'Отменен'),
    (SUCCEDED_STATUS, 'Успешно завершен'))

# Статусы заказа
PAID_STATUS = 'paid'
NOT_PAID_STATUS = 'not paid'

ORDER_STATUSES = (
    (PAID_STATUS, 'Оплачен'),
    (NOT_PAID_STATUS, 'Не оплачен')
)

# Способы сортировки
SORT_TYPES = ('new', '-new',
              'popular', '-popular',
              'price', '-price',
              'reviews', '-reviews')
