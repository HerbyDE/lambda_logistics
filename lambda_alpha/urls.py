from django.conf.urls import url, include
from django.conf.urls import (handler403, handler404, handler500)
from django.contrib.auth.views import logout as d_logout
from corelogistics import views as c_views
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^login/', c_views.login_user, name='login'),
    url(r'^logout/$', d_logout, {'next_page': '/'}, name='logout'),
    url(r'^$', c_views.landing_page, name='landing_page'),
    url(r'^core/', include('corelogistics.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^user/', include('usermgmt.urls')),
    url(r'^helpdesk/', include('helpdesk.urls')),
]

handler403 = 'helpdesk.views.forbidden'
handler404 = 'helpdesk.views.not_found'
handler500 = 'helpdesk.views.internal_error'
