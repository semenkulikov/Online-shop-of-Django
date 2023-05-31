from django import forms
from orderapp.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('city', 'address', 'delivery_type')
        widgets = {'delivery_type': forms.RadioSelect()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].required = True
        self.fields['address'].required = True
        for name, field in self.fields.items():
            field.widget.attrs['id'] = name
