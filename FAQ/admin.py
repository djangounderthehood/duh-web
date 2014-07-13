from django.contrib import admin

from .models import Entry


def make_published(modeladmin, request, queryset):
    queryset.publish()
make_published.short_description = "Mark selected entries as published"


class EntryAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'published', 'created_on')
    list_filter = ('published',)
    actions = [make_published]


admin.site.register(Entry, EntryAdmin)
