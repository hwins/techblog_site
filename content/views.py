from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView

from techblog.content.models import Post
from techblog.content.models import Post_Topic
from techblog.content.models import Topic


class PostListView(ListView):
    template_name = 'base_template.html'

    def get_queryset(self):
        return Post.objects.\
            filter(published=True).\
            order_by('-publish_date')


class PostDetailView(DetailView):
    template_name = 'post_template.html'

    def get(self, request, *args, year=None, month=None, day=None, slug=None):
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

    def get(self, request, topic=topic, *args, **kwargs):
        self.topic = topic
        return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        topic_detail = Topic.objects.get(topic_url_format=self.topic)
        posts_on_topic_list = Post_Topic.objects.\
            filter(topic_id=topic_detail.pk)
        queryset = Post.objects.\
            filter(post_topic__in=posts_on_topic_list)
        return queryset
