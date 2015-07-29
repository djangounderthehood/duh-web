from django.shortcuts import render

from sponsors.models import Sponsor
from attendees.models import Attendee


def home(request):
    if request.user.is_staff:
        sponsors = Sponsor.objects.all()
    else:
        sponsors = Sponsor.objects.live()
    return render(request, 'home.html', {'sponsors': sponsors})

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
