# urls.py for shobiz_staff

from django.conf.urls import patterns, url

from staff import views

urlpatterns = patterns('',
    url(r'^$', views.StaffMenuView.as_view(), name='staff_menu'),
    url(r'^customer/$', views.CustomerListView.as_view(), name='customer_list'),
    url(r'^customer/(?P<pk>\d+)/$', views.CustomerDetailView.as_view(), name='customer_detail'),
    url(r'^customer/create/$', views.CustomerCreateView.as_view(), name='customer_create'),
    url(r'^customer/phone/$', views.CustomerDetailByPhone.as_view(), name='customer_phone_lookup'),
    url(r'^customer/update/(?P<pk>\d+)/$', views.CustomerUpdateView.as_view(), name='customer_update'),
    )
