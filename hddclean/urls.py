from django.conf.urls import patterns, url
from hddclean import views

urlpatterns = patterns('',
    url(r'^clean', views.clean, name='clean'),
)
