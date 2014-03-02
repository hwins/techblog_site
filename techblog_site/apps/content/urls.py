from django.conf.urls import patterns, url

from techblog_site.apps.content.views import PostDetailView
from techblog_site.apps.content.views import PostListView
from techblog_site.apps.content.views import TopicPostListView


urlpatterns = patterns('techblog_site.apps.content.views',
    url(r'^$',
        PostListView.as_view()
        ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)',
        PostDetailView.as_view()
        ),
    url(r'^topics/(?P<topic>[-\w]+)$',
        TopicPostListView.as_view()
        ),
)

urlpatterns += patterns('django.contrib.flatpages.views',
    (r'^(?P<url>.*/)$', 'flatpage'),
)
