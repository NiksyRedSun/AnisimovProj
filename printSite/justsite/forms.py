from django import forms
from django.core.exceptions import ValidationError

from .models import Comments



class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text', 'rating']
        choices = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),)
        widgets = {
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'rating': forms.RadioSelect(choices=choices),
        }


    def __init__(self, ):


    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        rating = cleaned_data.get("rating")

        print(text)
        print(rating)


