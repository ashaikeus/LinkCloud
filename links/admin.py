from django.contrib import admin
from .models import Language, Link, Profile

admin.site.register(Language)
admin.site.register(Profile)

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('link', 'name', 'get_tags', 'language', 'author_id', 'private')

    @admin.display(description='Tags')
    def get_tags(self, instance):
        return ', '.join(tag.name for tag in instance.tags.all())