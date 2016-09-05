from django.conf.urls import url
from django.shortcuts import get_object_or_404

from .models import Redirection


def view(request, slug):
    redir = get_object_or_404(Redirection, slug=slug)
    return redir.go()


urlpatterns = [
    url(r'^(?P<slug>.+)/$', view, name='redirect'),
]
