from io import BytesIO

from django.http import HttpRequest, HttpResponse
import pandas as pd

from repositories import ProductSelectRepository

_product_repository = ProductSelectRepository()


def export_product_to_xls(request: HttpRequest, product_id: int)\
        -> HttpResponse:
    product = _product_repository.get_product_by_id(product_id=product_id)
    excel_file = BytesIO()
    excel_writer = pd.ExcelWriter(excel_file)
    df = pd.DataFrame({
        **{name_field.name: product.__getattribute__(str(name_field.name))
           for name_field in product._meta.fields}
    }, index=[product.pk])
    df['updated_at'] = product.updated_at.isoformat(sep=" ")
    df['created_at'] = product.created_at.isoformat(sep=" ")

    df.to_excel(excel_writer, sheet_name='product_data')
    excel_writer.close()
    excel_file.seek(0)

    response = HttpResponse(
        excel_file.read(),
        content_type='application/vnd.openxmlformats-'
                     'officedocument.spreadsheetml.sheet',
    )
    response[
        'Content-Disposition'
    ] = 'attachment; filename=test.xlsx'
    response['Set-Cookie'] = 'fileDownload=true; path=/'
    return response
