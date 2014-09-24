from functools import wraps
import json

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import mail_admins
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


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
    raw_data = json.loads(request.body.decode('utf-8'))
    reference = raw_data['reference']
    attendee = get_object_or_404(Attendee, reference=reference)
    if raw_data['state_name'] == 'void':  # ticket canceled
        attendee.delete()
        return HttpResponse('Attendee deleted.')

    data = get_model_data_from_raw(raw_data)
    attendee.update_with_data(data)
    return HttpResponse('Attendee updated.')
