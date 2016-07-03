from functools import wraps

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Participant
from .forms import ParticipantSignupForm


def timestamped(view):
    """
    Injects a current datetime on the request object at `request.timestamp`.
    Makes testing time-dependent views easy: just pass `timestamp` as kwarg to `get` or `post`.
    """

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        request.timestamp = request.environ.get('timestamp', timezone.now())
        return view(request, *args, **kwargs)

    return wrapper


@timestamped
def signup(request):
    if not settings.REGISTRATION_START <= request.timestamp <= settings.REGISTRATION_END:
        return redirect('registration_closed')

    if request.method == 'POST':
        form = ParticipantSignupForm(request.POST)
        if form.is_valid():
            participant = form.save()
            return redirect('signup_confirmation', email=participant.email)
    else:
        form = ParticipantSignupForm()

    return render(request, 'lottery/signup.html', {'form': form})


def signup_confirmation(request, email):
    participant = get_object_or_404(Participant, email=email)
    return render(request, 'lottery/signup_confirmation.html', {'participant': participant})


@timestamped
def registration_closed(request):
    return render(request, 'lottery/registration_closed.html', {
        'now': request.timestamp,
        'start': settings.REGISTRATION_START,
        'end': settings.REGISTRATION_END,
    })
