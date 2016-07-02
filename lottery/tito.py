import tablib

PERSONAL_COLUMNS = ['First Name', 'Last Name', 'Email', 'Expiry time', 'Redirect?']

# TODO: Check we've got *all* tickets named here
# Tito importer will protest if we don't list all current tickets categories
# Don't change order of individual and corporate tickets
TICKET_COLUMNS = ['Individual Ticket', 'Corporate Ticket', 'Scholarship Ticket']


def export_participants_to_csv(participants):
    """
    Export iterable of Participants to CSV format recognised by Tito RSVP
    importer.
    """

    headers = PERSONAL_COLUMNS + TICKET_COLUMNS
    data = tablib.Dataset(headers=headers)
    for p in participants:
        # Personal columns
        row = [p.first_name, p.last_name, p.email, p.batch.expires_at, 'Y']

        # Individual and corporate tickets
        row += ['Y' if p.individual else '', 'Y' if p.corporate else '']

        # Rest of the tickets
        row += [''] * (len(TICKET_COLUMNS) - 2)

        data.append(row)

    return data.csv
