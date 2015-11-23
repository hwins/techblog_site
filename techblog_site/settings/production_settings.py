"""
Django settings for techblog_site project.

"""
import os

path = os.path.abspath(os.path.dirname(__file__))
PROJECT_PATH = os.path.normpath(os.path.join(path,  ".."))
#control files are one level above project path
CONTROL_FILE_PATH = os.path.normpath(os.path.join(path,  "../.."))

# all sensitive data stored in control folder

with open(CONTROL_FILE_PATH + '/control/secret_key.private') as f:
    SECRET_KEY = f.read().strip()

DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['blog.howardwinston.com', ]

# access to /admin path is restricted via webserver
# this host name is for administrator
with open(CONTROL_FILE_PATH + '/control/admin_url.private') as f:
    ALLOWED_HOSTS.append(f.read().strip())


INSTALLED_APPS = (
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'endless_pagination',
    'tinymce',
    'techblog_site.apps.content',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'techblog_site.urls'

WSGI_APPLICATION = 'techblog_site.wsgi.application'

with open(CONTROL_FILE_PATH + '/control/db1_user.private') as f:
    DB1_USER = f.read().strip()
with open(CONTROL_FILE_PATH + '/control/db1_password.private') as f:
    DB1_PASSWORD = f.read().strip()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'techblog_site',
        'USER': DB1_USER,
        'PASSWORD': DB1_PASSWORD,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)

MEDIA_ROOT = '/home/techblog/techblog_site/media/'
MEDIA_URL = '/media/'

STATIC_ROOT = '/var/www/blog.howardwinston.com/static/'
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# TinyMCE settings
TINYMCE_DEFAULT_CONFIG = {
    'width': '760',
    'height': '480',
    'plugins': 'fullscreen,media,preview,paste,spellchecker',
    'theme': 'advanced',
    'relative_urls': False,
    'theme_advanced_toolbar_location': 'top',
    'theme_advanced_toolbar_align': 'left',
    'theme_advanced_buttons1': 'bold,italic,underline,strikethrough,|,' \
        'justifyleft,justifycenter,justifyright,justifyfull,|,forecolor,' \
        'formatselect,sub,sup,removeformat,charmap,|,bullist,numlist,|,' \
        'indent,outdent,|,link,unlink,anchor,image,media,|,visualaid,code,' \
        'preview,fullscreen',
    'theme_advanced_buttons2': 'undo,redo,|,cut,copy,paste,pasteword,' \
        'pastetext,selectall,|,cleanup,help,|,hr,|,spellchecker',
    'theme_advanced_buttons3': '',
    'theme_advanced_blockformats': 'p,pre,address,blockquote,h1,h2,h3,h4,' \
        'h5,h6,code',
    'plugin_preview_width': '800',
    'plugin_preview_height': '600',
    'paste_auto_cleanup_on_paste': 'true',
    'content_css': '/static/css/tinymce_edit.css',
    }

SITE_ID = 1

ENDLESS_PAGINATION_PER_PAGE = 5

HOLD_TWITTERJS = True
