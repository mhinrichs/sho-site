# urls.py for shobiz

from django.conf.urls import patterns, url

from shobiz import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^schedule/$', views.schedule, name='schedule'),
    url(r'^calendar/(?P<store_id>\w+)/(?P<emp_id>\w+)/(?P<year>\d+)/(?P<month>\d+)/$', views.calendar, name='calendar'),
    #url(r'^stores//$', views.stores, name='stores'),
    #url(r'^employees/$', views.employee, name='employees'),
    url(r'^time/$', views.time, name='time'),

)

