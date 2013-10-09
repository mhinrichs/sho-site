# urls.py for apo

from django.conf.urls import patterns, url

from apo import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^time/$', views.time, name='time'),
    url(r'^(?P<store_id>s\d+)/(?P<emp_id>e\d+)/(?P<year>\d+)/(?P<month>\d+)/$', views.month_schedule, name='test2'),


)

# Removed from URLS
# url(r'^(?P<store_id>s\d+)/(?P<emp_id>e\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.schedule, name='test'),



