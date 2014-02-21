import datetime

from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django import forms

from techblog.content.models import Topic, Post, Post_Topic


class PostTopicInline(admin.StackedInline):
    model = Post_Topic
    fk_name = 'post_id'


class PostAdminForm(forms.ModelForm):

    def clean_publish_date(self):
        if self.cleaned_data['published'] == True \
        and self.cleaned_data['publish_date'] == None:
            pub_date_error = 'Must set a publish date if published'
            raise forms.ValidationError(pub_date_error)
        else:
            return self.cleaned_data['publish_date']


class PostAdmin(ModelAdmin):
    model = Post
    form = PostAdminForm
    fields = ('title',
              'body',
              'published',
              'publish_date',
              )
    inlines = [PostTopicInline, ]
    list_display = ('title',
                    'published',
                    )

    def get_topics(self):
        return 'X'

    def save_model(self, request, obj, form, change):
        obj.slug = obj.title.strip().lower().replace(' ', '-')
        if obj.created == None:
            obj.created = datetime.datetime.now()
        if obj.published == None:
            obj.published = False
        obj.save()

admin.site.register(Post, PostAdmin)


class TopicAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TopicAdminForm, self).__init__(*args, **kwargs)
        self.fields['topic_parent'].queryset = \
        Topic.objects.filter(topic_parent_id__isnull=True)\
        .order_by('topic_name')

    def clean_topic_parent(self):
        """A topic can not point to itself as a parent and
        a child can not have a parent that is itself a child
        The parent choices are filtered so this under normal
        circumstances will never be needed, however if another
        user modifies topics this is a safeguard
        """
        if self.cleaned_data['topic_parent'] == None:
            return self.cleaned_data['topic_parent']
        else:
            if self.cleaned_data['topic_parent'].pk == self.instance.pk:
                child_parent_error = 'A topic cannot be its own parent'
                raise forms.ValidationError(child_parent_error)
            else:
                if self.cleaned_data['topic_parent'].topic_parent_id == None:
                    return self.cleaned_data['topic_parent']
                else:
                    parent_error = 'This parent is the child of other topics'
                    raise forms.ValidationError(parent_error)


class TopicAdmin(ModelAdmin):
    model = Topic
    form = TopicAdminForm
    fields = ('topic_name',
              'topic_parent',
              )

    list_display = ('topic_name',
                    'topic_parent'
                    )

admin.site.register(Topic, TopicAdmin)
