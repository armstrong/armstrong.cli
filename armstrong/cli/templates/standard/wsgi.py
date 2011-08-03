# Simple wsgi file for {{ project_name }}
import os
import sys

# Change this to reflect the environment you're in
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.development'

# Make sure that this project directory is first in the sys.path, or at least
# as close to first as can be reasonably assured in Python.
sys.path.insert(0, os.path.dirname(__file__))

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
