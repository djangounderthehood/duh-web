from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup$', views.signup, name='signup'),
    url(r'^thank-you/(?P<email>.*)$', views.signup_confirmation, name='signup_confirmation'),
    url(r'^closed$', views.registration_closed, name='registration_closed'),
]
