import tablib

PERSONAL_COLUMNS = ['First Name', 'Last Name', 'Email', 'Expiry time', 'Redirect?', 'Discount code']

# TODO: Check we've got *all* tickets named here
# Tito importer will protest if we don't list all current tickets categories
# Don't change order of individual, corporate and donation tickets
TICKET_COLUMNS = ['Individual Ticket', 'Corporate Ticket', 'Donation to Scholarship Programme',
    'Scholarship Ticket', 'Speaker Ticket', 'Organizer Ticket', 'Core Team Ticket', 'Sponsor Ticket', 
    'Staff Ticket']


def export_participants_to_csv(participants):
    """
    Export iterable of Participants to CSV format recognised by Tito RSVP
    importer.
    """

    headers = PERSONAL_COLUMNS + TICKET_COLUMNS
    data = tablib.Dataset(headers=headers)
    for p in participants:
        # Personal columns
        row = [p.first_name, p.last_name, p.email, p.batch.expires_at, 'Y', '']

        # Individual, corporate and donation tickets
        row += ['Y' if p.individual else '', 'Y' if p.corporate else '', 'Y']

        # Rest of the tickets
        row += [''] * (len(TICKET_COLUMNS) - 3)

        data.append(row)

    return data.csv
