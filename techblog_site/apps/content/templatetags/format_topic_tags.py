from django import template
from techblog_site.apps.content.models import Topic


register = template.Library()


@register.filter
def topic_tags_out(value):
    """This function takes a list of topic objects and will return
    HTML formatted with the topic name and a link to the appropriate
    topic page
    """
    formated_tags = ''
    if type(value) is list:
        for topic_detail in value:
            if type(topic_detail) is Topic:
                format_this_tag = '<div class="topic-tag">'
                format_this_tag += '<a href="/topics/%s">%s</a>' % \
                    (topic_detail.topic_url_format, topic_detail.topic_name)
                format_this_tag += '</div>'
            formated_tags += format_this_tag
    return formated_tags
