from django import forms
from productsapp.models import Review


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "text",

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs["class"] = "form-textarea"
        self.fields["text"].widget.attrs["name"] = "review"
        self.fields["text"].widget.attrs["id"] = "review"
        self.fields["text"].widget.attrs["placeholder"] = "Отзыв"
