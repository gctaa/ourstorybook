from base_settings import *
import os
import dj_database_url

ALLOWED_HOSTS = (
    '.herokuapp.com',
)

DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

REGISTRATION_TOKEN = 'HILT Institute'

INSTALLED_APPS = BASE_INSTALLED_APPS
