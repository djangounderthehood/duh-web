from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['day', 'start', 'title', 'speaker']
    change_list_template = 'smuggler/change_list.html'
