import csv
from collections import namedtuple

from django import forms
from django.utils.html import format_html

from slacker import Error as SlackError
from tomek import tomek  # 🚀

from .models import ClaimedInvitation, Invitation


CHANNELS = [
    ('#general', '#general'),
    ('#random', '#random'),
    ('#scholarships', '#scholarships'),
    ('#core', '#core'),
    ('#speakers', '#speakers'),
]


COC_LABEL = format_html("""I have read and agree with <a href="../../rules/">the rules of the slack channel</a>""")


class ClaimInvitationForm(forms.ModelForm):
    coc = forms.BooleanField(label=COC_LABEL, required=True)
    # choices will be set in __init__
    channels = forms.MultipleChoiceField(choices=CHANNELS, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = ClaimedInvitation
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        self.invitation = kwargs.pop('invitation')
        super(ClaimInvitationForm, self).__init__(*args, **kwargs)
        self._restrict_channels()

    def _restrict_channels(self):
        """
        Restrict (mutate) the choices for the channels fields based on the
        invitation object.
        """
        allowed = set(self.invitation.get_channels_from_ticket())
        choices = self.fields['channels'].choices
        self.fields['channels'].choices = [t for t in choices if t[0] in allowed]
        print(self.fields['channels'].choices)

    @tomek
    def save(self, commit=True):
        self.instance.invitation = self.invitation
        claimed_invitation = super(ClaimInvitationForm, self).save(commit=commit)
        # If the slack API sends us back an 'already invited' error, we treat
        # it as a regular form error. Otherwise, we let it bubble up.
        try:
            claimed_invitation.invite_to_slack(self.cleaned_data['channels'])
        except SlackError as e:
            if e.args[0] not in {'already_invited', 'already_in_team'}:
                raise
            error = forms.ValidationError("This email address already has an account on slack.", code='invalid')
            self.add_error('email', error)
            raise error

        return claimed_invitation


TitoCSVRow = namedtuple('TitoCSVRow', [
    'number',
    'ticket_created_date',
    'ticket_last_updated_date',
    'ticket',
    'ticket_full_name',
    'ticket_first_name',
    'ticket_last_name',
    'ticket_email',
    'ticket_company_name',
    'ticket_phone_number',
    'event',
    'void_status',
    'price',
    'ticket_reference',
    'tags',
    'unique_ticket_url',
    'unique_order_url',
    'order_reference',
    'order_name',
    'order_email',
    'order_company_name',
    'order_phone_number',
    'order_discount_code',
    'order_ip',
    'order_created_date',
    'order_completed_date',
    'payment_reference',
    'question_coc',
    'question_tshirt',
    'question_accessibility',
    'question_diet',
    'question_help',
    'question_sprints_sat',
    'question_sprints_sun',
    'question_name_badge',
    'conference_pass_lottery',
    'conference_pass_non_lottery'
])


class CSVFileField(forms.FileField):
    """
    A subclass of FileField that expects a CSV file and normalizes it to
    a python list of (named) tuples.
    """
    def __init__(self, *args, **kwargs):
        """
        tuple_class: Ideally a namedtuple class that will be used to validate/convert each row
        skip_rows: the number of rows to skip at the beginning (header)
        encoding: the encoding of the CSV file
        """
        self.tuple_class = kwargs.pop('tuple_class', tuple)
        self.skip_rows = kwargs.pop('skip_rows', 0)
        self.encoding = kwargs.pop('encoding', 'utf-8')
        super(CSVFileField, self).__init__(*args, **kwargs)

    def to_python(self, data):
        """
        Convert the uploaded CSV file to a Python list of (named) tuples.
        """
        f = super(CSVFileField, self).to_python(data)
        if f is None:
            return []
        # uploaded files are open in binary mode so we need to decode on the fly
        return list(self._gen_rows((line.decode(self.encoding) for line in f)))

    def _gen_rows(self, f):
        reader = csv.reader(f)
        for _ in range(self.skip_rows):
            next(reader)

        for i, row in enumerate(reader, self.skip_rows):
            try:
                yield self.tuple_class(*row)
            except TypeError:
                raise forms.ValidationError("Row %(row)d is invalid", params={'row': i}, code='invalid')


class UploadCSVForm(forms.Form):
    csv = CSVFileField(required=True, tuple_class=TitoCSVRow, skip_rows=1)

    @tomek
    def save(self):
        assert self.is_valid()
        created, skipped, updated = 0, 0, 0
        for row in self.cleaned_data['csv']:
            if 'donation' in row.ticket.lower():
                skipped += 1
                continue

            defaults={
                'first_name': row.ticket_first_name,
                'last_name': row.ticket_last_name,
                'email': row.ticket_email,
                'ticket_name': row.ticket,
            }

            invitation, was_created = Invitation.objects.update_or_create(
                ticket_id=row.ticket_reference,
                defaults=defaults,
            )

            if was_created:
                created += 1
            else:
                updated += 1
        return created, skipped, updated
