# -*- coding: utf-8 -*-

import os
import local_settings as ls

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_PATH = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]

TEMPLATE_ROOT = os.path.join(PROJECT_PATH, 'templates')
TEMPLATE_DIRS = (
    TEMPLATE_ROOT,)
CMS_TEMPLATES = ( # Templates for Django CMS
    ('template_1.html', 'Template One'),
    ('template_2.html', 'Template Two'),
    ('landing.html', 'Landing Template'),
)

# Media and Static Files
STATIC_PATH = os.path.join(PROJECT_PATH, 'static')
STATIC_ROOT = os.path.join(PROJECT_PATH, 'staticroot')
STATICFILES_DIRS = (
    STATIC_PATH,
)
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")
MEDIA_URL = '/media/'

# Email Info
ADMINS = ((ls.admin_name, ls.admin_email),)
MANAGERS = ADMINS
SERVER_EMAIL = ls.server_email
DEFAULT_FROM_EMAIL = ls.default_email
EMAIL_HOST = ls.email_host
EMAIL_PORT = ls.email_port
EMAIL_HOST_USER = ls.email_host_user
EMAIL_HOST_PASSWORD = ls.email_host_password
EMAIL_USE_TLS = True

# Database Info
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ls.db_name,
        'USER': ls.db_user,
        'PASSWORD': ls.db_pass,
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name

TIME_ZONE = 'Asia/Tokyo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
# https://docs.djangoproject.com/en/1.4/topics/i18n/translation/#how-django-discovers-language-preference

LANGUAGE_CODE = 'ja-jp'
# ugettext = lambda s: s #This is a lambda used with Django CMS to wrap the language setting
# LANGUAGES = [ #CMS languages
#     ('ja', ugettext('Japanese')),
# ]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ls.secret_key

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
    'zinnia.context_processors.version',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

ROOT_URLCONF = 'sho.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'sho.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.comments',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'shobiz', # app for sho
    'staff', # staff menu for shobiz
    #'shobizpos', eventual point of sale app for shobiz
    'cms',
    'mptt',
    'menus',
    'south',
    'sekizai',
    'zinnia',
    'tagging',
    'cmsplugin_zinnia',
    'cms.plugins.file',
    'cms.plugins.googlemap',
    'cms.plugins.link',
    'cms.plugins.picture',
    'cms.plugins.teaser',
    'cms.plugins.text',
    'cms.plugins.video',
    'cms.plugins.twitter',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'bootstrap3',
)

# auth and allauth settings

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

LOGIN_REDIRECT_URL = '/shobiz/'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email'],
        'METHOD': 'oauth2'
    }
}

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'THExSHOW'
ACCOUNT_PASSWORD_MIN_LENGTH = 6

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

