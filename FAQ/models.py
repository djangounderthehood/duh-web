from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class EntryQuerySet(models.QuerySet):
    def published(self):
        """
        Only include published items.
        """
        return self.filter(published=True)

    def publish(self):
        """
        Mark all items as published.
        """
        return self.update(published=True)


class Entry(models.Model):
    question = models.TextField(_("question"), help_text=_("You can use HTML."))
    answer = models.TextField(_("answer"), help_text=_("You can use HTML."))
    created_on = models.DateTimeField(_("created on"), default=timezone.now, editable=False)
    published = models.BooleanField(_("published"), default=False)

    objects = EntryQuerySet.as_manager()

    class Meta:
        verbose_name = _("entry")
        verbose_name_plural = _("entries")

    def __str__(self):
        return 'FAQ entry #{}'.format(self.pk)

    def publish(self):
        self.published = True
        self.save()
