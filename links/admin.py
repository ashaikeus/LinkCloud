from django.contrib import admin
from .models import Language, Link, Profile, Comment, Save, Report

admin.site.register(Language)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Save)
admin.site.register(Report)

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('link', 'name', 'get_tags', 'language', 'author', 'created_at', 'is_private', 'report_count')

    @admin.display(description='Tags')
    def get_tags(self, instance):
        return ', '.join(tag.name for tag in instance.tags.all())

    @admin.display(description='Report count')
    def report_count(self, instance):
        return instance.reports.count()