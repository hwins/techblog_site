from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView
from techblog_site.apps.content.models import Post
from techblog_site.apps.content.models import Post_Topic
from techblog_site.apps.content.models import Topic


def add_topic_list(queryset):
    """Add a list of topics for each post in the queryset."""
    for item_number, post in enumerate(queryset):
        topic_tags = []
        post_topic_queryset = Post_Topic.objects.\
            filter(post_id=post.pk)
        for tag in post_topic_queryset:
            try:
                get_topic_info = Topic.objects.get(id=tag.topic_id_id)
            except Topic.DoesNotExist:
                get_topic_info = None
            topic_tags.append(get_topic_info)
        queryset[item_number].topic_tags = topic_tags
    return queryset


class PostListView(ListView):
    """View for posts for both default home page and topic pages"""

    template_name = 'base_template.html'

    def get_queryset(self):
        queryset = Post.objects.\
            filter(published=True).\
            order_by('-publish_date')
        return add_topic_list(queryset)

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['listview_title'] = "Recent Posts"
        return context


class PostDetailView(DetailView):
    template_name = 'post_template.html'

    def get(self, request, year=None, month=None, day=None, slug=None):
        render_dictionary = {}
        post_object = Post.objects.get(
                                       slug__exact=slug,
                                       publish_date__year=year,
                                       publish_date__month=month,
                                       publish_date__day=day
                                       )
        render_dictionary['title'] = post_object.title
        render_dictionary['publish_date'] = post_object.publish_date
        render_dictionary['slug'] = post_object.slug
        render_dictionary['body_primary'] = post_object.body_primary
        render_dictionary['body_secondary'] = post_object.body_secondary

        return render(
                      request,
                      self.template_name,
                      render_dictionary,
                      )


class TopicPostListView(ListView):
    template_name = 'base_template.html'
    topic = None
    topic_name = None

    def get(self, request, topic=topic, *args, **kwargs):
        self.topic = topic
        return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        try:
            topic_detail = Topic.objects.get(topic_url_format=self.topic)
            self.topic_name = topic_detail.topic_name
        except ObjectDoesNotExist:
            raise Http404
        posts_on_topic_list = Post_Topic.objects.\
            filter(topic_id=topic_detail.pk)
        queryset = Post.objects.\
            filter(post_topic__in=posts_on_topic_list)
        return add_topic_list(queryset)

    def get_context_data(self, **kwargs):
        context = super(TopicPostListView, self).get_context_data(**kwargs)
        context['listview_title'] = self.topic_name + ' Topics'
        return context
