# urls.py for shobiz

from django.conf.urls import patterns, url

from shobiz import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.test, name='test'),
    url(r'^schedule/$', views.schedule, name='schedule'),
    url(r'^calendar/$', views.calendar, name='calendar'),
    url(r'^calendar/ajax/$', views.calendar_ajax, name='calendar_ajax'),
    url(r'^employees/$', views.employee, name='employees'),
    url(r'^time/$', views.time, name='time'),

)


# (?P<store_id>\w+)/(?P<emp_id>\w+)/(?P<year>\d+)/(?P<month>\d+)/


