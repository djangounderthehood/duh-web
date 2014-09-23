from django.shortcuts import render

from sponsors.models import Sponsor
from attendees.models import Attendee


def home(request):
    return render(request, 'home.html', {'sponsors': Sponsor.objects})

def coc(request):
    return render(request, 'coc.html', {})

def accessibility(request):
    return render(request, 'accessibility.html', {})

def travel(request):
    return render(request, 'travel.html', {})

def attendees(request):
    return render(request, 'attendees.html', {'attendees': Attendee.objects.all().order_by('?') })
