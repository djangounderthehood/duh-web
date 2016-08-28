from django.contrib.admin.helpers import AdminForm
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from .forms import ClaimInvitationForm, UploadCSVForm
from .models import ClaimedInvitation, Invitation
from .tito import TicketWebhookView


class TitoWebhookView(TicketWebhookView):
    def ticket_completed(self, request):
        if 'donation' in self.data['release_title'].lower():
            # Don't invite donation-only tickets
            return self.ok(request)

        invitation, _ = Invitation.objects.update_or_create(
            ticket_id=self.data['reference'],
            defaults={
                'first_name': self.data['first_name'],
                'last_name': self.data['last_name'],
                'email': self.data['email'],
                'ticket_name': self.data['release_title'],
            }
        )

        invitation.send_invite(resend=False)
        return self.ok(request)

    def ticket_updated(self, request):
        return self.ticket_completed(request)


class ClaimInvitationView(generic.CreateView):
    template_name = 'slakslakslak/claim.html'
    form_class = ClaimInvitationForm
    success_url = reverse_lazy('slakslakslak:success')

    def dispatch(self, request, token):
        self.invitation = get_object_or_404(Invitation, token=token)
        if self.invitation.is_claimed:
            return redirect('slakslakslak:already-claimed', token=token)
        return super(ClaimInvitationView, self).dispatch(request)

    def get_form_kwargs(self):
        kwargs = super(ClaimInvitationView, self).get_form_kwargs()
        kwargs['invitation'] = self.invitation
        return kwargs

    def get_initial(self):
        initial = super(ClaimInvitationView, self).get_initial()
        initial.update({
            'first_name': self.invitation.first_name,
            'last_name': self.invitation.last_name,
            'email': self.invitation.email,
            'channels': self.invitation.get_channels_from_ticket(),
        })
        return initial

    def form_valid(self, form):
        try:
            return super(ClaimInvitationView, self).form_valid(form)
        except ValidationError:
            return super(ClaimInvitationView, self).form_invalid(form)


class AlreadyClaimedView(generic.DetailView):
    slug_field = 'token'
    slug_url_kwarg = 'token'
    model = Invitation
    template_name = 'slakslakslak/already_claimed.html'


class SuccesClaimView(generic.TemplateView):
    template_name = 'slakslakslak/success_claim.html'


class RulesView(generic.TemplateView):
    template_name = 'slakslakslak/rules.html'


class UploadCSVView(generic.FormView):
    modeladmin = None
    form_class = UploadCSVForm
    template_name = 'slakslakslak/upload_csv.html'
    success_url = reverse_lazy('admin:slakslakslak_invitation_changelist')

    def form_valid(self, form):
        created, skipped, updated = form.save()
        msg = "Import successful: {} created, {} skipped, {} updated.".format(created, skipped, updated)
        messages.success(self.request, msg)
        return super(UploadCSVView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs = dict(self.modeladmin.admin_site.each_context(self.request), **kwargs)
        context = super(UploadCSVView, self).get_context_data(**kwargs)
        context.update({
            'adminform': AdminForm(form=context['form'], fieldsets=[(None, {'fields': ['csv']})], prepopulated_fields={}),
            'title': 'Import Invitations from Tito CSV',
            'has_file_field': True,

            # garbage to make admin work
            'opts': self.modeladmin.opts,
            'change': False,
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': True,
            'has_add_permission': True,
            'has_change_permission': True,
        })
        return context
