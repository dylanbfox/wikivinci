from django.conf.urls import patterns, include, url

from posts import views

urlpatterns = patterns('',
	url(r'^$', views.view_all, name='view_all'),
	url(r'^vote/$', views.vote, name='vote'),
	url(r'^add-link/$', views.add_link, name='add_link'),
	url(r'^(?P<slug>\w+(?:-\w+)*)/$', views.view, name='view')
)
