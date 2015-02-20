from django.conf.urls import patterns, url
from aureva_core import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.login_user, name='login'),
                       url(r'^logout/$', views.logout_user, name='logout'),
                       url(r'^user/(?P<username>[\w\d_]+)/$', views.user_profile, name='user_profile'),
                       url(r'^user/(?P<username>[\w\d_]+)/(?P<title>[\w\d_]+)/$', views.track, name='track'),
                       url(r'^account-settings/$', views.account_settings, name='account_settings'),
                       )