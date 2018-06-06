from django.conf.urls import url
from .views import parcel_list, request_detail, price_request

app_name = 'api'
urlpatterns = [
    url(r'^$', parcel_list, name='api_parcel_list'),
    url(r'^detail/(?P<pk>[0-9]+)/$', request_detail, name='api_parcel_detail'),
    url(r'^detail/pricing/(?P<pk>[0-9]+)/$', price_request, name='api_parcel_price'),
]