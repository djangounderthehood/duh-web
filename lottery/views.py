from django.shortcuts import render, redirect, get_object_or_404

from .models import Participant
from .forms import ParticipantSignupForm


def signup(request):
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
