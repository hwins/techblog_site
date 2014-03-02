import datetime
import string

from django import forms
from django.contrib import admin
from django.contrib.admin import options, widgets
from tinymce.widgets import TinyMCE

from techblog_site.apps.content import models
from django.forms.models import BaseInlineFormSet


class PostTopicFormSet(BaseInlineFormSet):
    """Only provide a drop down for child topics
    by filtering out the parents
    """
    def add_fields(self, form, index):
        super(PostTopicFormSet, self).add_fields(form, index)

        qs = models.Topic.objects.\
        filter(topic_parent_id__isnull=False).\
        order_by('topic_name')

        form.fields['topic_id'].queryset = qs


class PostTopicInline(admin.TabularInline):

    model = models.Post_Topic
    fk_name = 'post_id'
    extra = 1
    formset = PostTopicFormSet


class PostAdminForm(forms.ModelForm):

    body_primary = forms.CharField(widget=TinyMCE())
    body_secondary = forms.CharField(widget=TinyMCE())

    publish_date = forms.DateTimeField(
                                       required=False,
                                       widget=widgets.AdminSplitDateTime,
                                       )

    def clean_publish_date(self):
        """If published must have a published date
        but if NOT published - publish date must be empty
        """
        if self.cleaned_data['publish_date'] == None:
            if self.cleaned_data['published'] == True:
                pub_date_error = 'Must set a publish date if published'
                raise forms.ValidationError(pub_date_error)
            else:
                pass
        else:
            if self.cleaned_data['published'] == False:
                pub_date_error = 'Must publish if there is a publish date'
                raise forms.ValidationError(pub_date_error)

        return self.cleaned_data['publish_date']

    class Meta:
        pass


class PostAdmin(options.ModelAdmin):
    model = models.Post
    form = PostAdminForm
    fields = ('title',
              'slug',
              'created',
              'body_primary',
              'body_secondary',
              'published',
              'publish_date',
              )
    inlines = [PostTopicInline, ]
    list_display = ('title',
                    'published',
                    'publish_date',
                    )
    readonly_fields = ('slug',
                       'created',
                       )

    def save_model(self, request, obj, form, change):
        obj.slug = obj.title.strip().\
            lower().\
            replace(' ', '-')
        # remove any !@#$, etc.
        for p in string.punctuation:
            if p != '-':
                obj.slug = obj.slug.replace(p, '')
        obj.slug = obj.slug.rstrip('-')

        if obj.created == None:
            obj.created = datetime.datetime.now()
        if obj.published == None:
            obj.published = False
        obj.save()


admin.site.register(models.Post, PostAdmin)


class TopicAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TopicAdminForm, self).__init__(*args, **kwargs)
        self.fields['topic_parent'].queryset = \
        models.Topic.objects.filter(topic_parent_id__isnull=True)\
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


class TopicAdmin(options.ModelAdmin):
    model = models.Topic
    form = TopicAdminForm
    fields = ('topic_parent',
              'topic_name',
              'topic_url_format',
              )

    list_display = ('topic_parent',
                    'topic_name',
                    'topic_url_format',
                    )

    readonly_fields = ('topic_url_format',
                       )

    def save_model(self, request, obj, form, change):
        obj.topic_url_format = obj.topic_name.strip().\
            lower().\
            replace(' ', '-')
        # remove any !@#$, etc.
        for p in string.punctuation:
            if p != '-':
                obj.topic_url_format = obj.topic_url_format.replace(p, '')
        obj.topic_url_format = obj.topic_url_format.rstrip('-')
        obj.save()

admin.site.register(models.Topic, TopicAdmin)
