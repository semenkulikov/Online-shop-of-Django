CREATED_STATUS = 'created'
PENDING_STATUS = 'pending'
COMPLETED_STATUS = 'completed'
CANCELLED_STATUS = 'cancelled'
FAILED_STATUS = 'failed'

PAYMENT_STATUSES = ((CREATED_STATUS, 'Создан'),
                    (PENDING_STATUS, 'В обработке'),
                    (COMPLETED_STATUS, 'Выполнен'),
                    (CANCELLED_STATUS, 'Отменен'),
                    (FAILED_STATUS, 'Ошибочный'))
