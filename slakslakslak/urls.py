from django.conf.urls import url

from .views import (
    TitoWebhookView,
    ClaimInvitationView,
    AlreadyClaimedView,
    SuccesClaimView,
    RulesView,
)

urlpatterns = [
    url(r'^_titohook/$', TitoWebhookView.as_view(), name='titohook'),
    url(r'^(?P<token>.+)/claim/$', ClaimInvitationView.as_view(), name='claim'),
    url(r'^(?P<token>.+)/already-claimed/$', AlreadyClaimedView.as_view(), name='already-claimed'),
    url(r'^YAY/$', SuccesClaimView.as_view(), name='success'),
    url(r'^rules/$', RulesView.as_view(), name='rules'),
]
