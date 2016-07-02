from django.db import models
from django.utils import timezone

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
    participants_limit = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'batches'

    def __str__(self):
        return self.name


class Participant(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    ticket_type = models.CharField(max_length=200, choices=TICKET_TYPE_CHOICES)
    batch = models.ForeignKey(Batch, null=True)

    def __str__(self):
        return self.email
