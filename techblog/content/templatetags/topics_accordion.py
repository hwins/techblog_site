from django import template

from techblog.content.models import Post
from techblog.content.models import Post_Topic
from techblog.content.models import Topic


register = template.Library()

ABOUT_LINKS = '<h3>About</h3><ul>' + \
    '<li>link1</li>' + \
    '<li>link2</li>' + \
    '<li>link3</li>' + \
    '<li>link4</li></ul>'


class AccordionLine():
    """This class represents one line (tuple) of the menu accordion"""
    def __init__(self,
                 topic_group_name=None,
                 is_this_a_parent=False,
                 topic_name=None,
                 topic_count=0,
                 topic_url_format=None,
                 ):
        self.topic_group_name = topic_group_name
        self.is_this_a_parent = is_this_a_parent
        self.topic_name = topic_name
        self.topic_count = topic_count
        self.topic_url_format = topic_url_format

    def __repr__(self):
        return repr((self.topic_group_name,
                     self.is_this_a_parent,
                     self.topic_name,
                     self.topic_count,
                     self.topic_url_format,
                     ))


@register.simple_tag
def topics_accordion_out():
    """This function builds output for a Jquery accordion widget.
    The complication is that output must be sorted within parent
    groups, then children of those parents. The parents will be tagged
    differently.

    To do this a tuple for each line item is built that will include
    a temporary key for parents so they will be first, followed by
    their children.

    Note: accordion_out is built in reverse order for reasons that are
    explained in the comments in the code.
    """
    accordion_out = '<script>$( "#accordion" ).accordion();</script>'
    accordion_out = '</div>' + accordion_out
    accordion_list = []

    # only include topics that are in published post so
    # get a list of all the published posts
    published_posts = Post.objects.filter(published=True)

    # get a list of all available topics, counts
    for toa in Topic.objects.all():
        accordion_line = AccordionLine()
        if toa.topic_parent == None:
            # this line is a parent
            accordion_line.topic_group_name = toa.topic_name
            accordion_line.is_this_a_parent = True
            accordion_line.topic_name = toa.topic_name
            accordion_line.topic_count = 0
            accordion_line.topic_url_format = toa.topic_url_format
        else:
            # this line is a child
            accordion_line.topic_group_name = toa.topic_parent.__str__()
            accordion_line.is_this_a_parent = False
            accordion_line.topic_name = toa.topic_name
            # calculate the count of PUBLISHED posts for topic
            calc_count = \
                Post_Topic.objects.\
                filter(topic_id=toa.pk).\
                filter(post_id__in=published_posts).\
                count()
            accordion_line.topic_count = calc_count
            accordion_line.topic_url_format = toa.topic_url_format
        accordion_list.append(accordion_line)

    # sort list by group, parents last (false before true), then name
    # the reason for this is so any parent that has all children of 0
    # published counts will not print when processed
    accordion_list_sorted = sorted(
                                   accordion_list,
                                   key=lambda k:
                                   (
                                    k.topic_group_name,
                                    -k.is_this_a_parent,
                                    k.topic_name,
                                    ),
                                   reverse=True,
                                   )

    closing_ul_tag_printed = False
    published_count_for_group = 0
    for als in accordion_list_sorted:
        if als.is_this_a_parent:
            if published_count_for_group > 0:
                accordion_out = '<h3>%s</h3><ul>' % \
                    als.topic_group_name + \
                    accordion_out
                published_count_for_group = 0
            closing_ul_tag_printed = False
            published_count_for_group = 0
        else:
            if als.topic_count > 0:
                if not closing_ul_tag_printed:
                    accordion_out = '</ul>' + accordion_out
                    closing_ul_tag_printed = True
                # plural for post or posts
                if als.topic_count == 1:
                    s = ''
                else:
                    s = 's'
                accordion_out = '<li><a href="/topics/%s">%s </a> (%s ' % \
                    (als.topic_url_format, als.topic_name, als.topic_count) + \
                    'post' + s + ')</li>' + accordion_out
                published_count_for_group += als.topic_count

    accordion_out = ABOUT_LINKS + accordion_out

    accordion_out = '<div id="accordion">' + accordion_out
    return accordion_out
