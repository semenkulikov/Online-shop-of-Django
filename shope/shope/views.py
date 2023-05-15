from .tasks import send_order_confirmation_email
from django.http import HttpResponse
from .tasks import process_image


def create_order(request):
    # Логика создания заказа
    # ...

    # Отправка задачи Celery для отправки письма с подтверждением заказа
    send_order_confirmation_email.delay(order.id)

    # Ответ пользователю
    return HttpResponse('Заказ успешно оформлен.')


def process_image_view(request):
    # Логика получения пути к изображению
    image_path = '/path/to/image.jpg'

    # Отправка задачи Celery для обработки изображения
    result = process_image.delay(image_path)

    # Получение результата обработки изображения (необязательно)
    # processed_image_path = result.get()

    # Ответ пользователю
    return HttpResponse('Изображение отправлено на обработку.')
