from collections import namedtuple
import csv
import io
from optparse import make_option
from urllib.request import urlopen

from django.core.management.base import BaseCommand, CommandError
from attendees.models import Attendee

BaseAttendeeTuple = namedtuple('BaseAttendeeTuple', [
    'id',
    'created_date',
    'ticket_type',
    'full_name',
    'first_name',
    'last_name',
    'email',
    'event',
    'void_status',
    'price',
    'reference_',
    'tags',
    'ticket_url',
    'order_url',
    'order_reference',
    'order_name',
    'order_email',
    'order_discount',
    'order_ip',
    'order_start_date',
    'order_end_date',
    'payment_reference',
    'tshirt_size',
    'food_preference',
    'coc',
    'visible_',
    'twitter',
])


class AttendeeTuple(BaseAttendeeTuple):
    @property
    def visible(self):
        return self.visible_.lower() == 'yes'

    @property
    def reference(self):
        return self.reference_[:6]

    @property
    def category(self):
        """
        Try and guess the category (regular, sponsor, ...) by looking at the
        ticket type.
        """
        return Attendee.CATEGORY.guess(self.ticket_type)

    def get_model_data(self):
        return {
            'reference': self.reference,
            'name': self.full_name,
            'email': self.email,
            'twitter': self.twitter,
            'visible': self.visible,
            'category': self.category,
        }


class Command(BaseCommand):
    args = 'tito_csv_url'
    help = 'Updates the attendee table with the exported data from tito'
    option_list = BaseCommand.option_list + (
        make_option('--encoding',
            dest='encoding',
            default='utf-16',  # It seems that's what tito uses by default
            help="The CSV file's encoding"),
        )

    def handle(self, tito_csv_url, **options):
        encoding = options.get('encoding', 'utf-16')  # It seems tito uses utf-16 by default
        response = io.TextIOWrapper(urlopen(tito_csv_url), encoding=encoding, newline='')
        data = csv.reader(response)
        next(data)  # skip header row

        for row in data:
            item = AttendeeTuple(*row)

            defaults = item.get_model_data()
            reference = defaults.pop('reference')

            attendee, created = Attendee.objects.get_or_create(
                reference=reference,
                defaults=defaults,
            )

            # We don't want manual category changes to be overwritten
            del defaults['category']

            if created:
                self.stdout.write('Created attendee with reference %s.' % attendee.reference)
            elif any(getattr(attendee, attr) != value for attr, value in defaults.items()):
                attendee.update_with_data(defaults)
                self.stdout.write('Updated attendee with reference %s.' % attendee.reference)

        return
