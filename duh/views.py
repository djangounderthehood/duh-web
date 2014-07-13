from django.shortcuts import render

from interests.forms import RegisterInterestForm


def home(request):
    return render(request, 'home.html', {
        'interest_form': RegisterInterestForm(),
    })
