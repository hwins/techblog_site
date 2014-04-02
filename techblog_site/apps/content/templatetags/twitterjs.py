from django import template
from django.conf import settings


register = template.Library()

TWITTERJS = "<p><a class=\"twitter-timeline\" " + \
    "data-widget-id=\"333220753849851906\" " + \
    "href=\"https://twitter.com/hwins\">Tweets by @hwins</a></p> " + \
    "\n<script type=\"text/javascript\">\n" + \
    "<!--//--><![CDATA[// ><!--\n" + \
    "!function(d,s,id)" + \
    "{var js,fjs=d.getElementsByTagName(s)[0]," + \
    "p=/^http:/.test(d.location)?" + \
    "'http':'https';if(!d.getElementById(id))" + \
    "{js=d.createElement(s);" + \
    "js.id=id;js.src=p+" + \
    "\"://platform.twitter.com/widgets.js\";" + \
    "fjs.parentNode.insertBefore(js,fjs);}}" + \
    "(document,\"script\",\"twitter-wjs\");\n" + \
    "//--><!]]>\n</script>"


@register.simple_tag
def twitter_block_out():
    """Don't keep printing twitter block when in development"""
    if settings.HOLD_TWITTERJS:
        return "<p>twitter id = hwins</p>"
    else:
        return TWITTERJS
