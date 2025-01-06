from django import forms
from .models import Link, Language, Comment


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('link', 'name', 'description', 'tags', 'language', 'is_private')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
