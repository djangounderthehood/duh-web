from django.conf.urls import patterns, include, url
from django.contrib import admin

from duh import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^coc/$', views.coc, name='coc'),
    url(r'^accessibility/$', views.accessibility, name='accessibility'),
    url(r'^travel/$', views.travel, name='travel'),
    url(r'^attendees/$', views.attendees, name='attendees'),
    url(r'^talks/$', views.talks, name='talks'),
    url(r'^scholarship/$', views.scholarship, name='scholarship'),
    url(r'^schedule/$', views.schedule, name='schedule'),
    url(r'^admin/', include(admin.site.urls)),
)
