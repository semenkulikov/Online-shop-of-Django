from django import forms


class InputAmountForm(forms.Form):
    amount = forms.IntegerField(required=False, max_value=100)
    # поле для ввода количества
