from django.db import models
from django.shortcuts import redirect


class Redirection(models.Model):
    slug = models.SlugField(unique=True, help_text="Don't include leading/trailing slahes.")
    url = models.URLField()
    permanent = models.BooleanField(default=True)

    class Meta:
        verbose_name = '➡️'
        verbose_name_plural = '➡️➡️➡️'

    def go(self):
        return redirect(self.url, permanent=self.permanent)
