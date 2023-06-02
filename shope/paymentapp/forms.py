from django import forms


class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=19,
        min_length=13,
        required=True,
        label='card number')
    card_holder = forms.CharField(
        max_length=30,
        required=True,
        label='cardholder name')
    expiry_date = forms.DateField(
        required=True,
        input_formats=['%m/%y',],
        label='expiry date')
    cvv = forms.CharField(
        max_length=3,
        min_length=3,
        label='CVV/CVC code')
    total_sum = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='total sum (rub.)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total_sum'].widget.attrs['readonly'] = True
        self.label_suffix = ''
        self.fields['expiry_date'].widget.attrs['placeholder'] = 'mm/yy'
