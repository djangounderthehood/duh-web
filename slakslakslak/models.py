from functools import partial

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import get_template
from django.utils.crypto import get_random_string
from django.utils.functional import cached_property
from django.utils import timezone

from .managers import InvitationQuerySet
from .slack import get_connection as get_slack_connection, _convert_channels


class Invitation(models.Model):
    token = models.CharField(max_length=32, unique=True, default=partial(get_random_string, length=32), editable=False)

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    ticket_name = models.CharField(max_length=100)
    ticket_id = models.CharField(max_length=10, unique=True)

    created_on = models.DateTimeField(default=timezone.now)
    sent_on = models.DateTimeField(null=True, blank=True)

    objects = InvitationQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('slakslakslak:claim', kwargs={'token': self.token})

    @cached_property
    def is_claimed(self):
        try:
            self.claimed
        except ClaimedInvitation.DoesNotExist:
            return False
        return True

    def send_invite(self, request=None, resend=False):
        """
        Send an email with a link where the recipient can claim their slack
        invitation.
        """
        if not self.email:
            return 0

        if self.sent_on and not resend:
            return 0

        if request is None:
            domain = 'djangounderthehood.com'
            https = True
        else:
            site = get_current_site(request)
            domain = site.domain
            https = request.is_secure()

        tpl = get_template('slakslakslak/invite_email.txt')
        body = tpl.render({'invitation': self, 'domain': domain, 'https': https})

        sent = send_mail(
            subject='[Django Under the Hood 2016] Join our Slack channel',
            message=body,
            from_email='hello@djangounderthehood.com',
            recipient_list=[self.email],
        )
        self.sent_on = timezone.now()
        self.save(update_fields=['sent_on'])
        return sent

    def get_channels_from_ticket(self):
        """
        Generate the channels according to the ticket name.
        """
        ticket = self.ticket_name.lower()
        assert 'donation' not in ticket

        channels = ['#general', '#random']
        if 'scholarship' in ticket:
            channels.append('#scholarships')
        if 'core team' in ticket:
            channels.append('#core')
        if 'speaker' in ticket:
            channels.append('#speakers')
        if 'organizer' in ticket:
            channels.extend(['#scholarships', '#core', '#speakers'])

        return channels


class ClaimedInvitation(models.Model):
    invitation = models.OneToOneField('Invitation', related_name='claimed')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    claimed_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'claimed invitation'
        verbose_name_plural = 'claimed invitations'

    def invite_to_slack(self, channels=None):
        if settings.DEBUG:
            print("Skipped inviting to slack because settings.DEBUG=True")
            return
        if channels is None:
            channels = ['#general', '#random']
        public_slack = get_slack_connection('duth-2016')
        channels = _convert_channels(public_slack, channels)
        public_slack.users.invite(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            channels=channels,
        )
