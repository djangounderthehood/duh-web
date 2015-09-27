from datetime import datetime

from django.shortcuts import render
from django.utils import timezone

from sponsors.models import Sponsor
from attendees.models import Attendee


def home(request):
    ticket_sale_start = datetime(2015, 9, 17, 11, tzinfo=timezone.utc)
    if request.user.is_staff:
        sponsors = Sponsor.objects.all()
    else:
        sponsors = Sponsor.objects.live()
    return render(request, 'home.html', {
        'sponsors': sponsors,
        'ticket_sale_start': ticket_sale_start,
        'now': timezone.now(),
    })

def coc(request):
    return render(request, 'coc.html', {})

def accessibility(request):
    return render(request, 'accessibility.html', {})

def travel(request):
    return render(request, 'travel.html', {})

def attendees(request):
    return render(request, 'attendees.html', {'attendees': Attendee.objects.visible().order_by('?') })

def talks(request):
    return render(request, 'talks.html', {})

def scholarship(request):
    return render(request, 'scholarship.html', {})

def schedule(request):
    return render(request, 'schedule.html', {})