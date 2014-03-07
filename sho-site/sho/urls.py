# urls.py for sho-site

from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^shobiz/', include('shobiz.urls')),
    url(r'^staff/', include('staff.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^weblog/', include('zinnia.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('cms.urls')), # Must be at end of urlpatterns
)

if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns



