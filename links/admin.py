from django.contrib import admin
from .models import Tag, Language, Link, Profile

admin.site.register(Tag)
admin.site.register(Language)
admin.site.register(Link)
admin.site.register(Profile)