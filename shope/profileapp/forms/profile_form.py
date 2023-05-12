from django import forms
from profileapp.models import Profile
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

max_avatar_image_size = 2 * 1024 * 1024


class ProfileForm(forms.ModelForm):

    avatar_image = forms.ImageField(widget=forms.widgets.ClearableFileInput)
    phone_number = PhoneNumberField()

    class Meta:
        model = Profile
        fields = ('fio', 'avatar_image', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar_image'].required = False
        self.fields['fio'].required = True
        self.fields['phone_number'].required = False

    def clean_avatar_image(self):
        data = self.cleaned_data["avatar_image"]
        if data.size > max_avatar_image_size:
            raise ValidationError("Maximum avatar size is 2 Mb")

        return data
