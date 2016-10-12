from django.http import HttpResponse
from django.views.generic import ListView

from .models import Event


class ScheduleView(ListView):
    template_name = 'schedule/schedule.html'
    model = Event


class IcalTalkScheduleView(ScheduleView):
    def get_queryset(self):
        queryset = super(IcalTalkScheduleView, self).get_queryset()
        return queryset.talks()

    def get(self, request):
        calendar = self.get_queryset().as_ical()
        return HttpResponse(calendar.to_ical(),
                            content_type='text/calendar; charset=UTF-8')
