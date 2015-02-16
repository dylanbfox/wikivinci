from django.conf.urls import patterns, include, url

from posts import views

urlpatterns = patterns('',
	url(r'^$', views.view_all, name='view_all'),
	url(r'^topics/$', views.view_topics, name='topics'),
	url(r'^topics/suggest/$', views.ajax_suggest_tags, name='suggest_tags'),	
	url(r'^vote/$', views.vote, name='vote'),
	url(r'^add/$', views.add, name='add'),
	url(r'^(?P<slug>\w+(?:-\w+)*)/$', views.view, name='view'),
	url(r'^(?P<slug>\w+(?:-\w+)*)/flag/$', views.flag, name='flag'),
	url(r'^(?P<slug>\w+(?:-\w+)*)/go/$', views.go, name='go'),
	url(r'^(?P<slug>\w+(?:-\w+)*)/email/$', views.email, name='email'),
	url(r'^(?P<slug>\w+(?:-\w+)*)/favorite/$', views.favorite, name='favorite'),
)
