from django.conf.urls import patterns, include, url

from accounts import views

urlpatterns = patterns('',
	url(r'^login/$', views.account_login, name='login'),
	url(r'^login/twitter/$', views.twitter_login, name='twitter_login'),
	url(r'^twitter-add-email/$', views.twitter_add_email, name='twitter_add_email'),
	url(r'^register/$', views.account_register, name='register'),
	url(r'^logout/$', views.account_logout, name='logout'),
	url(r'^(?P<username>.+)/feed/$', views.feed, name='feed'),	
	url(r'^(?P<username>.+)/settings/$', views.account_settings, name='settings'),	
	url(r'^(?P<username>.+)/$', views.profile, name='profile'),
)
