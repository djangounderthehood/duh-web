from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {})

def coc(request):
    return render(request, 'coc.html', {})

def accessibility(request):
    return render(request, 'accessibility.html', {})

def travel(request):
    return render(request, 'travel.html', {})
