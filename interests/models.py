from django.core import signing
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class InterestManager(models.Manager):
    def get_from_token(self, token):
        """
        Return the Interest instance matching the given token.
        If the token is malformed, a BadSignature error will be raised.
        If the token is valid but no matching model is found, a DoesNotExist is
        raised instead.
        """
        email = signing.loads(token, salt=Interest._SALT)
        return self.get(email=email)


class Interest(models.Model):
    _SALT = 'interests.models.Interest'
    email = models.EmailField(_("email"), primary_key=True)
    name = models.CharField(_("name"), max_length=200, blank=True)
    message = models.TextField(_("message"), blank=True)
    created_on = models.DateTimeField(_("created on"), default=timezone.now, editable=False)

    objects = InterestManager()

    class Meta:
        verbose_name = _("interest")
        verbose_name_plural = _("interests")

    def __str__(self):
        if self.name:
            return '{} <{}>'.format(self.name, self.email)
        return self.email

    @property
    def token(self):
        return signing.dumps(self.email, salt=self._SALT)
