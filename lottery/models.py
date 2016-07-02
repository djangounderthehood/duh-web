from datetime import timedelta
from django.db import models
from django.db.transaction import atomic
from django.utils import timezone

RSVP_VALIDITY_HOURS = 72

INDIVIDUAL_TICKET = 'individual'
CORPORATE_TICKET = 'corporate'
TICKET_TYPE_CHOICES = [
    (INDIVIDUAL_TICKET, 'Individual Ticket'),
    (CORPORATE_TICKET, 'Corporate Ticket'),
]


class Batch(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    assigned_at = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=200)
    tickets = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'batches'

    def __str__(self):
        return self.name

    @property
    def assigned(self):
        return bool(self.assigned_at)

    @property
    def expires_at(self):
        if not self.assigned:
            return None

        return self.assigned_at + timedelta(hours=RSVP_VALIDITY_HOURS)

    @atomic
    def assign_participants(self):
        if self.assigned:
            raise ValueError('Batch %s has already been assigned' % self.id)

        self.assigned_at = timezone.now()
        self.save()

        ids_query = Participant.objects.filter(batch=None).order_by('?')[:self.tickets]
        return Participant.objects.filter(id__in=ids_query).update(batch=self)


class Participant(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    ticket_type = models.CharField(max_length=200, choices=TICKET_TYPE_CHOICES)
    batch = models.ForeignKey(Batch, null=True, blank=True, related_name='participants')

    def __str__(self):
        return self.email

    @property
    def individual(self):
        return self.ticket_type == INDIVIDUAL_TICKET

    @property
    def corporate(self):
        return self.ticket_type == CORPORATE_TICKET
