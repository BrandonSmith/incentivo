import settings

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'incentivo_bolsa'

DATABASE_USER = 'incentivo'
DATABASE_PASSWORD = 'sugar1tassi'
DATABASE_HOST = 'mysql.incentivo.dreamhosters.com'

MEDIA_ROOT = '/home/incentivo/media.incentivo.org.br'
OTHER_MEDIA_ROOT = '/home/incentivo/django_projects/incentivo/resources/'

MEDIA_URL = ''

ADMIN_MEDIA_PREFIX = 'http://mediabolsa.dreamhosters.com/admin_media/'

TEMPLATE_DIRS = (
    "/home/incentivo/django_projects/incentivo",
    "/home/incentivo/django_src/django/contrib/databrowse/templates",
)
