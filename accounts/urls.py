from django.conf.urls import patterns, include, url

from accounts import views

urlpatterns = patterns('',
	url(r'^login/$', views.account_login, name='login'),
	url(r'^register/$', views.account_register, name='register'),
)