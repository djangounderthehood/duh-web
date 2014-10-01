from django.contrib import admin

from .models import Attendee

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference', 'email', 'twitter', 'visible', 'category')
    list_filter = ('visible', 'category')
    search_fields = ['name', 'reference', 'email', 'twitter']
