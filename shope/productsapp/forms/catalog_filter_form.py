from django import forms
import re


class CatalogFilterForm(forms.Form):
    """
    Форма валидации параметров фильтра в каталоге
    """
    name = forms.CharField(max_length=50, required=False)
    price_range = forms.CharField(max_length=30, required=False)
    free_delivery = forms.BooleanField(required=False)
    in_stock = forms.BooleanField(required=False)
    sort = forms.CharField(max_length=20, required=False)
    tag = forms.CharField(max_length=50, required=False)
    price_min = forms.IntegerField(min_value=0, required=False)
    price_max = forms.IntegerField(min_value=0, required=False)

    def clean(self):
        """
        Проверка корректности и нормализация диапазона цены,
        в противном случае ценовой диапазон не учитывается в фильтре
        """
        cleaned_data = super().clean()
        price_range = cleaned_data.get('price_range')
        if re.fullmatch(r'^\d+;\d+$', price_range):
            price_min, price_max = map(int, price_range.split(';'))
            if price_min < price_max:
                cleaned_data['price_min'] = price_min
                cleaned_data['price_max'] = price_max
        return cleaned_data

    def clean_sort(self):
        """
        Проверка корректности параметра сортировки,
        в противном случае применяется значение по умолчанию
        """
        sort = self.cleaned_data.get('sort')
        if sort in ('new', '-new', 'popular', '-popular',
                    'price', '-price', 'reviews', '-reviews'):
            return sort
        else:  # параметр sort отуствтует или некорректен
            return '-reviews'
