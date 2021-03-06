from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from filebrowser.sites import site

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/filebrowser/', include(site.urls)),
                       url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/tinymce/', include('tinymce.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^media/(?P<path>.*)$',
                           'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}
                           ),
                       url(r'^', include('techblog_site.apps.content.urls')),
)
