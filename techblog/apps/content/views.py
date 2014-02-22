from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView
from techblog.apps.content.models import Post
from techblog.apps.content.models import Post_Topic
from techblog.apps.content.models import Topic


class PostListView(ListView):
    template_name = 'base_template.html'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['listview_title'] = "Recent Posts"
        return context

    def get_queryset(self):
        queryset = Post.objects.\
            filter(published=True).\
            order_by('-publish_date')
        # add a list of topics for each post in the queryset
        for item_number, post in enumerate(queryset):
            topic_tags = Post_Topic.objects.filter(post_id=post.pk)
            queryset[item_number].topic_tags = topic_tags
        return queryset


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
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TopicPostListView, self).get_context_data(**kwargs)
        context['listview_title'] = self.topic_name
        return context
