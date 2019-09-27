from .base import *

DEBUG = True

SECRET_KEY = 'some super secret key here wefc23d'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'name_the_db.sqlite3'),
    }
}

ALLOWED_HOSTS = ['yours_site.com']