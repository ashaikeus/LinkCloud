from django import forms
from .models import Link, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('link', 'name', 'description', 'tags', 'language', 'is_private')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
