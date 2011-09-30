# Production settings for {{ project_name }}
from settings.defaults import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Change this to work with your default production database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                       # Or path to database file if using sqlite3.
        'USER': '',                       # Not used with sqlite3.
        'PASSWORD': '',                   # Not used with sqlite3.
        'HOST': '',                       # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                       # Set to empty string for default. Not used with sqlite3.
    }
}

# URL configuration to use in production mode
ROOT_URLCONF = 'urls.production'

# Attempt to load any settings from settings.local_production, but ignore any
# errors complaining about them not being present.
try:
    from settings.local_production import *
except ImportError, e:
    pass
