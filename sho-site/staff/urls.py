# urls.py for shobiz_staff

from django.conf.urls import patterns, url

from staff import views

urlpatterns = patterns('',
    url(r'^$', views.StaffMenuView.as_view(), name='staff_menu'),
    url(r'^customers/$', views.CustomerListView.as_view(), name='customer_list'),
    url(r'^customers/(?P<pk>\d+)/$', views.CustomerDetailView.as_view(), name='customer_detail'),
    url(r'^customers/create/$', views.CustomerCreateView.as_view(), name='customer_create'),
    url(r'^customers/phone/$', views.CustomerDetailByPhone.as_view(), name='customer_phone_lookup'),
    url(r'^customers/update/(?P<pk>\d+)/$', views.CustomerUpdateView.as_view(), name='customer_update'),
    )
