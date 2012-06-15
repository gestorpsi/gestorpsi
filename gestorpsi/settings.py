"""
Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import os
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_DISABLED = False # display "system is currently under maintenance" message instead login if True

ADMINS = (
     ('GestorPsi', 'webmaster@gestorpsi.com.br'),
)

GESTORPSI_DEFAULT_INSCRIPTION_TAX = '500.00'


#EMAIL_FROM = 'GestorPsi <webmaster@gestorpsi.com.br>'
EMAIL_FROM = 'peixegama@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'peixegama@gmail.com'
EMAIL_HOST_PASSWORD = 'quackquack22'
EMAIL_HOST_PORT = 465
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_FROM


MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gestor',                      # Or path to database file if using sqlite3.
        'USER': 'gestor',                      # Not used with sqlite3.
        'PASSWORD': 'gestor',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'pt_BR'
LANGUAGE_CODE = 'pt_BR'

_ = lambda s: s

LANGUAGES = (
    ('pt_BR', _('Brazilian Portuguese')),
    ('en_US', _('English')),
)


SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# cookies
LOCALE_PATHS = ()
LANGUAGE_COOKIE_NAME = 'gestor_language'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = '/home/gestor/demo/gestorpsi/media/' *************AQUI****************
MEDIA_ROOT = 'media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://192.168.0.200:8000/media/' *************AQUI****************
MEDIA_URL = 'http://127.0.0.1:8000/media/'

ADMIN_URL = '/admin/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/admin_media/' *************AQUI****************
ADMIN_MEDIA_PREFIX = '/admin_media/'


# Make this unique, and don't share it with anybody.
#SECRET_KEY = '3%$a^8zp51kg@=4dz_o@gwiuvt2062kt8cimpjzg)ri37-5cq*'
SECRET_KEY  = '4&(dsaHDH532Dd7Az!#hJk*%231_0!ds87s*dw3-fxz$dfs43x'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',    
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'swingtime.context_processors.current_datetime',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'gestorpsi.middleware.threadlocals.ThreadLocals',
    #'gestorpsi.util.usertimeout.UserTimeout',
    #'gestorpsi.util.showqueries.ShowQueries',
)

ROOT_URLCONF = 'gestorpsi.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #"/home/gestor/demo/gestorpsi/templates"
    #"/home/gestorpsi/Desenvolvimento/Django/gestorpsi/templates"
    os.path.join(PROJECT_ROOT_PATH, "templates"),
    os.path.join(PROJECT_ROOT_PATH, "async_tasks/templates"),
    os.path.join(PROJECT_ROOT_PATH, "boleto/templates"),
    os.path.join(PROJECT_ROOT_PATH, "gcm/templates"),
    os.path.join(PROJECT_ROOT_PATH, "util/templatetags"),
)

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',  
    'django_extensions',  
    'gestorpsi.authentication',
    'gestorpsi.util',
    'gestorpsi.sponsor',
    'gestorpsi.organization',
    'gestorpsi.careprofessional',
    'gestorpsi.contact',
    'gestorpsi.place',
    'gestorpsi.device',
    'gestorpsi.service',
    'gestorpsi.client',
    'gestorpsi.admission',
    'gestorpsi.referral',
    'gestorpsi.phone',
    'gestorpsi.address',
    'gestorpsi.person',
    'gestorpsi.employee',
    'gestorpsi.document',
    'gestorpsi.internet',
    'gestorpsi.upload',
    'gestorpsi.support',
    'gestorpsi.cbo',
    'gestorpsi.demographic',
    #'gestorpsi.socioeconomic',  <--- TO BE IMPLEMENTED SOON
    'gestorpsi.ehr',
    'gestorpsi.report',
    'gestorpsi.boleto',
    
    'swingtime',
    'registration',
    'south',
    'gestorpsi.online_messages',
    'rosetta',
    'gestorpsi.schedule',
    'reversion',
    'gestorpsi.frontend', #load at last
    'gestorpsi.gcm',
    'notification',
    'smart_selects',
    'djcelery',
    'kombu.transport.django',
    'django_extensions'
)

AUTHENTICATION_BACKENDS = (
    #'gestorpsi.util.auth_backends.CustomUserModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    
)

#CUSTOM_USER_MODEL = 'authentication.CustomUser'
AUTH_PROFILE_MODULE = 'authentication.profile'

#login
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login'

DEFAULT_EMAIL_MIMETYPE = 'html'

#SESSION_COOKIE_AGE = 7200      # 2 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SESSION_ENGINE = 'django.contrib.sessions.backends.file'  # default is django.contrib.sessions.backends.db

# used by authentication view
PASSWORD_RETIRES = 3

# CACHE #
#CACHE_BACKEND = 'locmem://'
#CACHE_MIDDLEWARE_KEY_PREFIX = ''
#CACHE_MIDDLEWARE_SECONDS = 1

PAGE_RESULTS = 8

SWINGTIME_SETTINGS_MODULE = 'gestorpsi.schedule.settings'

# a workaround to exclude referrals discharged reason == canceled to use in referral reports
REFERRAL_DISCHARGE_REASON_CANCELED = 20

# registration
ACCOUNT_ACTIVATION_DAYS=7




#django celery: task scheduling package
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_VHOST = "gestorpsi"
BROKER_USER = "danielcj"
BROKER_PASSWORD = "jcleinad"
BROKER_BACKEND = "djkombu.transport.DatabaseTransport"

CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("gestorpsi.async_tasks.tasks", )

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

import djcelery
djcelery.setup_loader()
#django celery: task scheduling package

