from django.conf.urls import url
from . import views

app_name = 'helpdesk'
urlpatterns = [
    url(r'^$', views.index, name='index')
]