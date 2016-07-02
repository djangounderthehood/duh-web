from django.contrib import admin
from django.contrib import messages

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
    list_display = ['pk', 'name', 'tickets', 'assigned_at', 'created_at']
    list_display_links = ['pk', 'name']
    readonly_fields = ['created_at', 'assigned_at']
    actions = ['assign_participants']

    def assign_participants(self, request, queryset):
        if len(queryset) != 1:
            msg = 'Use this action on one Batch at a time'
            self.message_user(request, msg, level=messages.ERROR)
            return

        batch = queryset[0]
        if batch.assigned:
            msg = 'Batch %d has already been assigned' % batch.id
            self.message_user(request, msg, level=messages.ERROR)
            return

        assigned_participants = batch.assign_participants()
        msg = '%d participants assigned to %s' % (assigned_participants, batch)
        level = messages.SUCCESS if assigned_participants == batch.tickets else messages.WARNING
        self.message_user(request, msg, level=level)
