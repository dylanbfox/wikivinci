from django.conf.urls import patterns, include, url
from django.contrib import admin

# need following lines for local MEDIA URL
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),    
    url(r'^posts/', include('posts.urls', namespace='posts')),
    url(r'^comments/', include('comments.urls', namespace='comments')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
