from django import forms
from .models import Link, Language, Comment

# class LinkForm(forms.ModelForm):
#     class Meta:
#         model = Link
#         fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
