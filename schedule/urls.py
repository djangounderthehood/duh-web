from django.conf.urls import url

from .views import ScheduleView, IcalTalkScheduleView

urlpatterns = [
    url(r'^$', ScheduleView.as_view(), name='schedule'),
    url(r'^talks/ical/$', IcalTalkScheduleView.as_view(), name='talks-ical'),
]
