from django.conf.urls import patterns, url
from testwipe import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^main/', views.main, name='main'),
    url(r'^wipe/', views.wipe, name='wipe'),
    url(r'^clone/', views.clone, name='clone'),
)
