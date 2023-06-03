from coreapp.utils.products_comparison_list import ProductsComparisonList


def count_comparis_block(request):
    """
    Контекстный процессор для отображения
    количества товаров в списке сравнения
    """

    _comparison_service = ProductsComparisonList()
    count_comparis = _comparison_service.comparison_list_size(
        request=request
    )
    context = {
        "count_comparis": count_comparis
    }

    return context
