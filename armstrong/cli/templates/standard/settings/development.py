# Development settings for {{ project_name }}
from settings.defaults import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Change this to work with your default development database
DATABASES = {
    'default': {
        #{% if demo %}
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': project_dir('./demo/demo_database.sqlite3'),                       # Or path to database file if using sqlite3.
        #{% else %}
        'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                       # Or path to database file if using sqlite3.
        #{% endif %}
        'USER': '',                       # Not used with sqlite3.
        'PASSWORD': '',                   # Not used with sqlite3.
        'HOST': '',                       # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                       # Set to empty string for default. Not used with sqlite3.
    }
}

# URL configuration to use in development mode
ROOT_URLCONF = 'urls.development'


# Attempt to load any settings from settings.local_development, but ignore any
# errors complaining about them not being present.
try:
    from settings.local_development import *
except ImportError, e:
    pass
