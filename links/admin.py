from django.contrib import admin
from .models import Language, Link, Profile, Comment

admin.site.register(Language)
admin.site.register(Profile)
admin.site.register(Comment)

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('link', 'name', 'get_tags', 'language', 'author', 'private')

    @admin.display(description='Tags')
    def get_tags(self, instance):
        return ', '.join(tag.name for tag in instance.tags.all())