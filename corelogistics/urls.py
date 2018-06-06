from django.conf.urls import url
from . import views
from django.contrib import admin

admin.autodiscover()

app_name='corelogistics'
urlpatterns = [
    url(r'^$', views.landing_page, name='home'),
    url(r'^parcel/new/', views.create_parcel, name='new_parcel'),
    url(r'^parcel/new/confirm/(?P<pk>\d+)$', views.confirm_parcel, name='confirm_parcel'),
    url(r'^parcel/new/delete/(?P<pk>\d+)$', views.cancel_parcel, name='delete_parcel'),
    url(r'^parcel/track/', views.track_parcel, name='track'),
    url(r'^parcel/list/$', views.parcel_list, name='parcel_list'),
    url(r'^parcel/detail/(?P<pk>\d+)$', views.parcel_detail, name='parcel_detail'),
    url(r'^parcel/status/update_admin/(?P<pk>\d+)$', views.status_update_admin, name='parcel_update_admin'),
    url(r'^parcel/status/reset_admin/(?P<pk>\d+)$', views.delivery_reset_admin, name='parcel_reset_admin'),
    url(r'^parcel/status/fail_admin/(?P<pk>\d+)$', views.delivery_fails_admin, name='parcel_delivery_fail_admin'),
    url(r'^parcel/status/update/(?P<pk>\d+)$', views.status_update, name='parcel_update'),
    url(r'^parcel/status/reset/(?P<pk>\d+)$', views.delivery_reset, name='parcel_reset'),
    url(r'^parcel/status/fail/(?P<pk>\d+)$', views.delivery_fails, name='parcel_delivery_fail'),
    url(r'^parcel/dashboard/$', views.dashboard, name='dashboard'),
    url(r'^driver/log/$', views.driver_logbook_initial, name='driver_log')
]