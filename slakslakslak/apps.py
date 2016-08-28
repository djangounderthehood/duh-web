from django.apps import AppConfig

from . import slack


class MonkeyPatchingConfig(AppConfig):
    name = 'slakslakslak'
    verbose_name = '💬💬💬'

    def ready(self):
        slack._monkeypatch_user_invite()
