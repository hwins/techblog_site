# this module will override default settings with
# development environment values

import os
#
path = os.path.abspath(os.path.dirname(__file__))
PROJECT_PATH = os.path.normpath(os.path.join(path,  ".."))
#
DEBUG = True
TEMPLATE_DEBUG = True
#
MEDIA_ROOT = os.path.join(PROJECT_PATH, '../media/')
MEDIA_URL = '/media/'

STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static/'),
)
#
ENDLESS_PAGINATION_PER_PAGE = 2

HOLD_TWITTERJS = True
