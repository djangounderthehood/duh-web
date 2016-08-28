import sys

from django.core.management.base import BaseCommand
from django.utils import timezone

from slakslakslak.models import Invitation


class Command(BaseCommand):
    help = 'Send pending invitation emails'

    def handle(self, **kwargs):
        pending = Invitation.objects.unsent()

        msg = "This will send {} emails. Are you sure you want to continue? (y/N)".format(pending.count())
        self.stdout.write(msg, ending=' ')
        if input('').lower() not in {'y', 'yes', 'oui', 'ja', 'tak', '👍'}:
            self.stdout.write('Got it, cancelling now...')
            sys.exit(1)

        for invitation in pending:
            try:
                self.stdout.write('Sending email to {}...'.format(invitation.email), ending=' ')
                invitation.send_invite()
                invitation.sent_on = timezone.now()
                invitation.save(update_fields=['sent_on'])
            except Exception:
                self.stdout.write('ERROR')
            else:
                self.stdout.write('OK')
