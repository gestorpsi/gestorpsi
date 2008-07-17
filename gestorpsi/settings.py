# Django settings for app project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('GestorPsi', 'webmaster@gestorpsi.com.br'),
)

EMAIL_FROM = 'GestorPsi <webmaster@gestorpsi.com.br>'

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'gestor'             # Or path to database file if using sqlite3.
DATABASE_USER = 'gestor'             # Not used with sqlite3.
DATABASE_PASSWORD = 'gestor'         # Not used with sqlite3.
DATABASE_HOST = 'dbhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt'

_ = lambda s: s

LANGUAGES = (
    ('pt', _('Brazilian Portuguese')),
    ('en', _('English')),
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

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media_admin/' *************AQUI****************
ADMIN_MEDIA_PREFIX = '/media_admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3%$a^8zp51kg@=4dz_o@gwiuvt2062kt8cimpjzg)ri37-5cq*'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'gestorpsi.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #"/home/gestor/demo/gestorpsi/templates"
    #"/home/gestorpsi/Desenvolvimento/Django/gestorpsi/templates"
    "templates"
)

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    #'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    #'gestorpsi.organization',
    #'gestorpsi.contacts',
    'gestorpsi.place',
    'gestorpsi.client',
    'gestorpsi.phone',
    'gestorpsi.address',
    'gestorpsi.person',
    'gestorpsi.document',
    'gestorpsi.internet',
    'gestorpsi.frontend', #load at last
)

DEFAULT_EMAIL_MIMETYPE = 'html'

# CACHE #
#CACHE_BACKEND = 'locmem://'
#CACHE_MIDDLEWARE_KEY_PREFIX = ''
#CACHE_MIDDLEWARE_SECONDS = 1

