from django.db import models
from typing import Final

from taggit.managers import TaggableManager

_LINK_MAX_LENGTH: Final = 255
_STRING_MAX_LENGTH: Final = 80


class Language(models.Model):
    name = models.CharField(max_length=_STRING_MAX_LENGTH, unique=True)

    def __str__(self) -> str:
        return self.name


class Link(models.Model):
    link = models.CharField(max_length=_LINK_MAX_LENGTH, unique=True)
    name = models.CharField(max_length=_STRING_MAX_LENGTH, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tags = TaggableManager()
    language = models.ForeignKey(Language, related_name='links', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    author = models.ForeignKey('Profile', related_name='created_links', on_delete=models.SET_NULL,
                                  null=True, blank=True)
    private = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name or self.link


class Profile(models.Model):
    name = models.CharField(max_length=_STRING_MAX_LENGTH)
    avatar_url = models.CharField(max_length=_LINK_MAX_LENGTH, null=True, blank=True)
    likes = models.ManyToManyField(Link, related_name='likers', null=True, blank=True)
    languages = models.ManyToManyField(Language, related_name='profiles', null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey('Profile', related_name='created_comments', on_delete=models.SET_NULL, null=True)
    link = models.ForeignKey('Link', related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.id}: on {self.link} by {self.author}"