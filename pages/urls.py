from django.conf.urls import patterns, include, url

from pages import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^contributors/$', views.contributors, name='contributors'),
)
