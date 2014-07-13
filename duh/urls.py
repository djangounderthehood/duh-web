from django.conf.urls import patterns, include, url
from django.contrib import admin

from duh import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^interest/', include('interests.urls')),
    url(r'^FAQ/', include('FAQ.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
