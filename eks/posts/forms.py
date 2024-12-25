from django import forms
from django.core.exceptions import ValidationError

from eks.posts.models import Post


class PostForm(forms.ModelForm):

    def clean_body(self):
        value = self.cleaned_data['body']
        if len(value) < 10:
            raise ValidationError("Posts must be longer than 10 characters.")
        return value
    class Meta:
        model = Post
        fields = ["body"]
