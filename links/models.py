from django.db import models
from typing import Final

_LINK_MAX_LENGTH: Final = 255
_STRING_MAX_LENGTH: Final = 80


class Tag(models.Model):
    name = models.CharField(max_length=_STRING_MAX_LENGTH, unique=True)

    def __str__(self) -> str:
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=_STRING_MAX_LENGTH, unique=True)

    def __str__(self) -> str:
        return self.name


class Link(models.Model):
    link = models.CharField(max_length=_LINK_MAX_LENGTH, unique=True)
    name = models.CharField(max_length=_STRING_MAX_LENGTH, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='links')
    language = models.ForeignKey(Language, related_name='links', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    author_id = models.ForeignKey('Profile', related_name='created_links', on_delete=models.SET_NULL,
                                  null=True, blank=True)

    def __str__(self) -> str:
        return self.name or self.link


class Profile(models.Model):
    name = models.CharField(max_length=_STRING_MAX_LENGTH)
    avatar_url = models.CharField(max_length=_LINK_MAX_LENGTH)
    likes = models.ManyToManyField(Link, related_name='likers')
    comments = models.ManyToManyField(Link, related_name='commenters')
    languages = models.ManyToManyField(Language, related_name='profiles')

    def __str__(self) -> str:
        return self.name
