from functools import wraps
import json

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import mail_admins
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Attendee


QUESTION_IDS = {
    1005591: 'tshirt',
    1005592: 'food',
    1005593: 'coc',
    1005872: 'visible',
    1005873: 'twitter',
}


def tito_auth_required(view):
    """
    A view decorator that makes sure the webhook requests originate from tito.
    This is done by looking at the 'custom' key in the JSON data given by tito.
    """
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        raw_data = json.loads(request.body.decode('utf-8'))
        if raw_data['custom'] != settings.TITO_AUTH_TOKEN:
            mail_admins('Webhook fail', request.body)
            raise PermissionDenied
        return view(request, *args, **kwargs)

    return wrapped


def get_model_data_from_raw(data):
    """
    Extract the relevant data from the huge blob provided by tito.
    """
    answers = dictify_answers(data['answers'])
    return {
        'name': data['name'],
        'email': data['email'],
        'twitter': answers.get('twitter'),
        'visible': answers.get('visible', '').lower() == 'yes'
    }


def dictify_answers(answers):
    """
    Tito's webhook gives us answers to questions in a list with items like this:
    {
        "question":{
            "title":"What's your t-shirt size?",
            "description":"",
            "id":1005591
        },
        "response":"Male XXL"
    }
    This function returns a simple dict keyed by the question (taken from
    QUESTION_IDS) and with the answers as values.
    """
    d = {}
    for answer in answers:
        question_id = answer['question']['id']
        question = QUESTION_IDS[question_id]
        response = answer['response']
        d[question] = response
    return d


@require_POST
@csrf_exempt
@tito_auth_required
def ticket(request):
    if request.META.get('X-Webhook-Name') == 'ticket.created':
        # We don't handle initial creation because there's not enough
        # information in the given data to create a meaningful entry.
        return HttpResponse('Skipped')  # TODO: is there a more appropriate response here?

    raw_data = json.loads(request.body.decode('utf-8'))
    reference = raw_data['reference']
    try:
        attendee = Attendee.objects.get(reference=reference)
    except Attendee.DoesNotExist:
        category = Attendee.CATEGORY.guess(raw_data['release'])
        attendee = Attendee(reference=reference, category=category)  # will be saved by update_with_data

    if not attendee.email:
        # Not sure why but tito sends webhooks for incomplete tickets (ie no email).
        # There isn't much we can do with that data so we skip it.
        return HttpResponse('Skipped')  # TODO: is there a more appropriate response here?

    if raw_data['state_name'] == 'void':  # ticket canceled
        attendee.delete()
        return HttpResponse('Attendee deleted.')

    data = get_model_data_from_raw(raw_data)
    attendee.update_with_data(data)
    return HttpResponse('Attendee updated.')
