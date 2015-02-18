from django.conf.urls import patterns, include, url

from topics import views

urlpatterns = patterns('',
	url(r'^$', views.view_all, name='view_all'),
	url(r'^(?P<slug>\w+(?:-\w+)*)/$', views.view, name='view'),
	url(r'^(?P<slug>\w+(?:-\w+)*)/apply/$', views.apply, name='apply'),
	url(r'^(?P<slug>\w+(?:-\w+)*)/add-post/$', views.add_post, name='add_post'),
)
