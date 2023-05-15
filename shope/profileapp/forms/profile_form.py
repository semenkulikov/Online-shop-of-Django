from django import forms
from profileapp.models import Profile
from django.core.exceptions import ValidationError
from django.conf import settings


class ProfileForm(forms.ModelForm):
    avatar_image = forms.ImageField(widget=forms.widgets.ClearableFileInput)
    phone_number = forms.CharField()

    class Meta:
        model = Profile
        fields = ('fio', 'avatar_image', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar_image'].required = False
        self.fields['fio'].required = True
        self.fields['phone_number'].required = True

    def clean_avatar_image(self):
        data = self.cleaned_data["avatar_image"]
        if data.size > settings.MAX_AVATAR_IMAGE_SIZE:
            raise ValidationError("Maximum avatar size is 2 Mb")
        return data
