from django.db import models



class InvitationQuerySet(models.QuerySet):
    def sent(self):
        """
        Invitations that have been sent already.
        """
        return self.filter(sent_on__isnull=False)

    def unsent(self):
        """
        Invitations that have not been sent yet.
        """
        return self.filter(sent_on__isnull=True)

    def claimed(self):
        """
        Invitations that have been claimed already.
        """
        return self.filter(claimed__isnull=False)

    def unclaimed(self):
        """
        Invitations that have not been claimed yet.
        """
        return self.filter(claimed__isnull=True)
