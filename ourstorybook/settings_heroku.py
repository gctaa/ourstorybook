from base_settings import *
import os
import dj_database_url

ALLOWED_HOSTS = (
    '.herokuapp.com',
)

DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

#CACHE = {}
#
# TODO: Figure out how to use memcache on heroku!
# 
#

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

INSTALLED_APPS = BASE_INSTALLED_APPS
