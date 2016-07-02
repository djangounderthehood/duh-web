from django.contrib import admin

from .models import Batch, Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['pk', 'first_name', 'last_name', 'email', 'ticket_type', 'batch', 'created_at']
    list_display_links = ['pk', 'first_name', 'last_name', 'email']
    list_filter = ['ticket_type', 'batch']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['created_at']


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'participants_limit', 'assigned_at', 'created_at', ]
    list_display_links = ['pk', 'name']
    readonly_fields = ['created_at']
