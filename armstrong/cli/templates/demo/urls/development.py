"""
Add any additional URLs that should only be available when using the the
settings.development configuration.

See ``urls.defaults`` for a list of all URLs available across both
configurations.
"""
from .defaults import *

urlpatterns += patterns('',

    # Examples:
    # url(r'^$', '{{ project_name }}.views.debug', name='debug'),
    # url(r'^{{ project_name }}/', include('{{ project_name }}.debug.urls')),
)
