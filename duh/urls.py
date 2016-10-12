from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from duh import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^coc/$', views.coc, name='coc'),
    url(r'^accessibility/$', views.accessibility, name='accessibility'),
    url(r'^travel/$', views.travel, name='travel'),
    url(r'^blog/', include('tinyblog.urls', namespace='blog')),
    #url(r'^attendees/$', views.attendees, name='attendees'),
    #url(r'^talks/$', views.talks, name='talks'),
    url(r'^scholarship/$', views.scholarship, name='scholarship'),
    url(r'^schedule/$', views.schedule, name='schedule'),
    url(r'^_schedule/', include('schedule.urls', namespace='schedule')),
    url(r'^sprints/$', views.sprints, name='sprints'),
    url(r'^team/', include('organizers.urls', namespace='organizers')),
    url(r'^tickets/', include('lottery.urls')),
    url(r'^admin/', include('smuggler.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^slack/', include('slakslakslak.urls', namespace='slakslakslak')),
    url(r'^r/', include('rocks.urls', namespace='rocks')),
]

# Serve uploaded files in DEBUG mode
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
