from datetime import datetime

from django.conf import settings
from django.shortcuts import render, redirect
from django.utils import timezone

from sponsors.models import Sponsor
from attendees.models import Attendee


def home(request):
    if request.user.is_staff:
        sponsors = Sponsor.objects.all()
    else:
        sponsors = Sponsor.objects.live()
    return render(request, 'home.html', {
        'sponsors': sponsors,
        'ticket_sale_start': settings.REGISTRATION_START,
        'now': timezone.now(),
    })


def coc(request):
    return render(request, 'coc.html')


def accessibility(request):
    return render(request, 'accessibility.html')


def travel(request):
    return render(request, 'travel.html')


def attendees(request):
    return render(request, 'attendees.html', {
        'attendees': Attendee.objects.visible().order_by('?')
    })


def talks(request):
    return render(request, 'talks.html')


def scholarship(request):
    return render(request, 'scholarship.html')


def sprints(request):
    return render(request, 'sprints.html', {})


def livestream(request):
    return redirect('https://www.youtube.com/channel/UC9T1dhIlL_8Va9DxvKRowBw/live')


def dinners(request):
    return redirect('https://docs.google.com/spreadsheets/d/18O80dlYqra39I7Tq46p7Qa4yCbgVHCFpVawgICwUFEc/edit#gid=0')
