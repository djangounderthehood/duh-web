from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render
from django.templatetags.static import static
from django.utils.html import format_html

from .models import ClaimedInvitation, Invitation
from .views import UploadCSVView


def combine_name(obj):
    return '{} {}'.format(obj.first_name, obj.last_name).strip()
combine_name.short_description = 'Name'


class YesNoBaseFilter(admin.SimpleListFilter):
    YES = '1'
    NO = '0'

    def lookups(self, request, model_admin):
        return (
            (self.YES,  'Yes'),
            (self.NO ,  'No'),
        )


class EmailSentFilter(YesNoBaseFilter):
    title = 'invitation sent'
    parameter_name = 'sent'

    def queryset(self, request, queryset):
        if self.value() == self.YES:
            return queryset.sent()
        if self.value() == self.NO:
            return queryset.unsent()


class InvitationClaimedFilter(YesNoBaseFilter):
    title = 'invitation claimed'
    parameter_name = 'claimed'

    def queryset(self, request, queryset):
        if self.value() == self.YES:
            return queryset.claimed()
        if self.value() == self.NO:
            return queryset.unclaimed()


@admin.register(ClaimedInvitation)
class ClaimedInvitationAdmin(admin.ModelAdmin):
    list_display = [combine_name, 'email', 'claimed_on']
    search_fields = ['first_name', 'last_name', 'email']


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = [combine_name, 'email', 'ticket_name', 'ticket_id', 'sent_on', 'is_claimed']
    search_fields = ['first_name', 'last_name', 'email', 'ticket_id']
    list_filter = [EmailSentFilter, InvitationClaimedFilter, 'ticket_name']
    list_select_related = ['claimed']
    actions = ['send_invite']

    def get_urls(self):
        """
        Add an "upload CSV" URL.
        """
        urls = super(InvitationAdmin, self).get_urls()
        upload_csv = UploadCSVView.as_view(modeladmin=self)
        return [
            url(r'^upload-csv/$', self.admin_site.admin_view(upload_csv), name='slakslakslak_invitation_upload')
        ] + urls

    def send_invite(self, request, queryset):
        """
        Admin action for sending invite email.

        Note: the email will be sent even if it's been sent before.
        """
        sent = 0
        total = len(queryset)
        for invitation in queryset:
            sent += invitation.send_invite(request=request, resend=True)

        messages.success(request, "%d/%d invitation emails sent successfully" % (sent, total))
    send_invite.short_description = "Send invitation emails"

    def is_claimed(self, obj):
        """
        A boolean-style icon with a link to the claimed invitation if it exists.
        """
        try:
            claimed = obj.claimed
        except ClaimedInvitation.DoesNotExist:
            return format_html('<img src="{}" alt="False" />', static('admin/img/icon-no.svg'))
        return format_html('<a href="{}"><img src="{}" alt="True" /></a>',
            reverse('admin:slakslakslak_claimedinvitation_change', args=[claimed.pk]),
            static('admin/img/icon-yes.svg'),
        )
    is_claimed.short_description = 'Claimed'
