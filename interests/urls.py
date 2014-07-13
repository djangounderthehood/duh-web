from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.CreateView.as_view(), name='register-interest'),
    url(r'^(?P<token>[a-zA-Z0-9:_-]+)/$', views.UpdateView.as_view(), name='update-interest'),
    url(r'^(?P<token>[a-zA-Z0-9:_-]+)/delete/$', views.DeleteView.as_view(), name='delete-interest'),
)
