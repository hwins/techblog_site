# this module will override default settings with
# development environment values


# # #
DEBUG = True
TEMPLATE_DEBUG = True

STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static/'),
)
#  
ENDLESS_PAGINATION_PER_PAGE = 2
# 
HOLD_TWITTERJS = True

