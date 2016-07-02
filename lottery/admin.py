from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.text import slugify

from .tito import export_participants_to_csv
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
    actions = ['assign_participants', 'export_to_csv']

    def assign_participants(self, request, queryset):
        if len(queryset) != 1 or queryset[0].assigned:
            msg = 'Action available only for one, unassigned Batch'
            self.message_user(request, msg, level=messages.ERROR)
            return

        batch = queryset[0]
        assigned_participants = batch.assign_participants()

        msg = '%d participants assigned to %s' % (assigned_participants, batch)
        level = messages.SUCCESS if assigned_participants == batch.tickets else messages.WARNING
        self.message_user(request, msg, level=level)

    def export_to_csv(self, request, queryset):
        if len(queryset) != 1 or not queryset[0].assigned:
            msg = 'Action available only for one, assigned Batch'
            self.message_user(request, msg, level=messages.ERROR)
            return

        batch = queryset[0]
        participants = batch.participants.order_by('email')
        csv = export_participants_to_csv(participants)

        response = HttpResponse(csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % slugify(batch)
        return response
