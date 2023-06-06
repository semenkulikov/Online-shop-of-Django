from io import BytesIO

from django.http import HttpRequest, HttpResponse
import pandas as pd

from repositories import OrderRepository

_order_repository = OrderRepository()


def export_orders_to_xls(request: HttpRequest)\
        -> HttpResponse:
    orders = _order_repository.get_all()
    excel_file = BytesIO()
    excel_writer = pd.ExcelWriter(excel_file)
    for order in orders:
        df = pd.DataFrame({
            **{name_field.name: order.__getattribute__(str(name_field.name))
               for name_field in order._meta.fields}
        }, index=[order.pk])
        df['updated_at'] = order.updated_at.isoformat(sep=" ")
        df['created_at'] = order.created_at.isoformat(sep=" ")

        df.to_excel(excel_writer, sheet_name=f'order_data_{order.id}')

    excel_writer.close()
    excel_file.seek(0)

    response = HttpResponse(
        excel_file.read(),
        content_type='application/vnd.openxmlformats-'
                     'officedocument.spreadsheetml.sheet',
    )
    response[
        'Content-Disposition'
    ] = 'attachment; filename=products.xlsx'
    response['Set-Cookie'] = 'fileDownload=true; path=/'
    return response
