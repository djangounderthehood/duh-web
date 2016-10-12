from datetime import datetime, timedelta

import icalendar

from django.db import models
from django.utils import timezone


class EventQuerySet(models.QuerySet):
    def as_ical(self, **kwargs):
        calendar = icalendar.Calendar()
        for k, v in kwargs.items():
            calendar[k] = v
        for event in self:
            if event.is_blank:
                continue
            calendar.add_component(event.as_ical())
        return calendar

    def talks(self):
        return self.exclude(speaker='')


class Event(models.Model):
    day = models.DateField()
    venue = models.CharField(max_length=50)
    venue_url = models.URLField()
    start = models.TimeField()
    duration = models.PositiveIntegerField(default=60, help_text="In minutes")
    is_break = models.BooleanField(default=False)

    title = models.CharField(max_length=200, blank=True, help_text="Leave blank to create gaps in the schedule")
    speaker = models.CharField(max_length=100, blank=True)

    objects = EventQuerySet.as_manager()

    class Meta:
        ordering = ('day', 'start')

    @property
    def is_blank(self):
        return not self.title

    @property
    def day_grouping(self):
        """
        Used for grouping events by day, so that events starting after midnight
        still get grouped with the previous day.
        """
        if self.start.hour < 2:
            return self.day - timedelta(days=1)
        return self.day

    def get_css_class(self):
        classes = ['session']
        if self.is_break:
            classes.append('break')
        if self.duration != 60:
            classes.append('session-{}min'.format(self.duration))
        return ' '.join(classes)

    @property
    def dt_start(self):
        return timezone.make_aware(datetime.combine(self.day, self.start))

    @property
    def dt_end(self):
        return self.dt_start + timedelta(minutes=self.duration)

    @property
    def ical_uid(self):
        app, model = self._meta.label_lower.split('.')
        return "{}{}@2016.duth.rocks".format(model, self.pk)

    @property
    def ical_summary(self):
        if not self.speaker:
            return self.title
        return '{} - {}'.format(self.speaker, self.title)

    def as_ical(self):
        """
        Return a representation of the current talk as an icalendar.Event.
        """
        event = icalendar.Event()
        event.add("dtstart", self.dt_start)
        event.add("dtend", self.dt_end)
        event.add("uid", self.ical_uid)
        event.add("summary", self.ical_summary)
        event.add("location", "{}, Amsterdam, NL".format(self.venue))
        return event
