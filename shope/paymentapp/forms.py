from django import forms


class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=19,
        min_length=13,
        required=True,
        label='card number (12-19 digits)')
    card_holder = forms.CharField(
        max_length=30,
        required=True,
        label='cardholder name')
    expiry_date = forms.DateField(
        required=True,
        input_formats=['%m/%y',],
        widget=forms.DateInput,
        label='expiry date')
    cvv = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.PasswordInput,
        label='CVV/CVC')
    total_sum = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.HiddenInput,
        label='total sum (rub.)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['expiry_date'].widget.attrs['placeholder'] = 'mm/yy'
        self.fields['expiry_date'].widget.attrs['class'] = 'input_small'
        self.fields['cvv'].widget.attrs['class'] = 'input_small'
