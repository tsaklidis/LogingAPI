from .base import *

DEBUG = True

SECRET_KEY = 'some super secret key here wefc23d'

# Set the database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'name_the_db.sqlite3'),
    }
}

# For PostgreSQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': '',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

ALLOWED_HOSTS = ['yours_site.com']