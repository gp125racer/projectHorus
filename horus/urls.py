"""horus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from falcon import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url('^login', auth_views.login, {'template_name':'falcon/login.html'}),
    url('^logout', auth_views.logout, {'template_name':'falcon/logout.html', 'next_page':'/'}),
    url('^register', views.RegisterView.as_view()),
    url('^flightplan/create', views.CreateFlightPlanView.as_view(), name='flightplan_create'),
    url('^flightplan/list', views.ListFlightPlanView.as_view(), name='flightplan_list'),
    url('^flightplan/delete/(?P<pk>\d+)$', views.DeleteFlightplanView.as_view(), name='flightplan_delete'),
    url('^device/create', views.RegisterDeviceView.as_view(), name='device_create'),
    url('^device/list', views.ListDeviceView.as_view(), name='device_list'),
    url('^device/delete/(?P<pk>\d+)$', views.DeleteDeviceView.as_view(), name='device_delete'),
    url('^device/edit/(?P<pk>\d+)$', views.UpdateDeviceView.as_view(), name='device_update'),
    url('^mission/create', views.CreateMissionView.as_view(), name='mission_create'),
    url('^mission/list', views.ListMissionView.as_view(), name='mission_list'),
    url('^mission/delete/(?P<pk>\d+)$', views.DeleteMissionView.as_view(), name='mission_delete'),
    url('^mission/edit/(?P<pk>\d+)$', views.UpdateMissionView.as_view(), name='mission_update'),
    url('^mission/fetch/(?P<device_uid>[^/]+)/$', views.FetchMissionView.as_view(), name="mission_fetch"),
    url('^mission/accept/(?P<muid>[^/]+)/(?P<duid>[^/]+)/$', views.AcceptMissionView.as_view(), name="mission_accept"),
    url('^mission/completed/(?P<mission_uid>[^/]+)/$', views.CompletedMissionView.as_view(), name='mission_completed'),
    url('^mission/start/(?P<mission_id>\d+)$', views.StartMissionView.as_view(), name='mission_start'),
    url('^mission/stop/(?P<mission_id>\d+)$', views.StopMissionView.as_view(), name='mission_stop'),
    url('^mission/liveview/(?P<mission_uid>[^/]+)/$', views.LiveMissionView.as_view(), name='mission_liveview'),
]
