from django.conf.urls import url
from . import views

app_name = 'usermgmt'
urlpatterns = [
    url(r'^$', views.index, name='usermgmt_index'),
]