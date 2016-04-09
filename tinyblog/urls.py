from django.conf.urls import url

from .views import post_detail, post_list

urlpatterns = [
    url(r'^$', post_list, name='index'),
    url(r'^article/(?P<slug>[-\w]+)/$', post_detail, name='article'),
]
