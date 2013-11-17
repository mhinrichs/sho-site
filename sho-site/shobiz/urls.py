# urls.py for shobiz

from django.conf.urls import patterns, url

from shobiz import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^calendar/$', views.calendar, name='calendar'),
    url(r'^schedule/(?P<store_id>\w+)/(?P<emp_id>\w+)/(?P<year>\d+)/(?P<month>\d+)/$', views.schedule, name='schedule'),
    url(r'^time/$', views.time, name='time'),

)
