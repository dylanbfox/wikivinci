from django.conf.urls import patterns, include, url

from comments import views

urlpatterns = patterns('',
	url(r'^add/$', views.add, name='add'),
	url(r'^vote/$', views.vote, name='vote'),
	url(r'^delete/$', views.delete, name='delete'),
)
