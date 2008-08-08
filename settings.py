DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Brandon Smith', 'brandon@16cards.com'),
)

MANAGERS = (
	('contato', 'contato@incentivo.org.br'),
)

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/home/brandon/user/django_projects/incentivo/db'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/New York'

# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
LANGUAGE_CODE = 'pt-BR'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = ''
OTHER_MEDIA_ROOT = '/home/brandon/user/django_projects/incentivo/resources/'
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'wx%272im+hme0(n6*8hvusr*gxk)-5@dx+j2h13m149+=2774z'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'incentivo.urls'

TEMPLATE_DIRS = (
    "/home/brandon/user/django_projects/incentivo",
    "/home/brandon/user/django_src/django/contrib/databrowse/templates",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.i18n',
    'django.core.context_processors.auth',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    #'django.contrib.databrowse',
    'django.contrib.flatpages',
    'django.contrib.formtools',
    'bolsa',
    'faq',
    #'contact_form',
)

# EMAIL_HOST = 'mail.incentivo.org.br'
EMAIL_HOST = 'incentivo.dreamhosters.com'
EMAIL_HOST_USER = 'contato@incentivo.org.br'
EMAIL_HOST_PASSWORD = 'BYEnc4Sw'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'contato@incentivo.org.br'
SERVER_EMAIL = 'contato@incentivo.org.br'
