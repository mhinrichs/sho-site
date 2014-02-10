# urls.py for shobiz

from django.conf.urls import patterns, url

from shobiz import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^calendar/$', views.calendar, name='calendar'),
    url(r'^calendar/ajax/$', views.calendar_ajax, name='calendar_ajax'),
    url(r'^employee/$', views.employee, name='employee'),
    url(r'^schedule/$', views.schedule, name='schedule'),
    url(r'^appointment/$', views.make_appointment, name='make_appointment'),
    url(r'^success/$', views.success, name='success'),
)


