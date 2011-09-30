"""
Contains URL patterns for a basic API using `Tastypie`_.

.. _tastypie: https://github.com/toastdriven/django-tastypie
"""
from django.conf.urls.defaults import patterns, include, url

from apis.api import v1_api


urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
)