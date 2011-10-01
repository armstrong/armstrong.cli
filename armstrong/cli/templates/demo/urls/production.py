"""
Add any additional URLs that should only be available when using the the
settings.production configuration.

This is useful for having a production location for debugging utilities where
you do not want them on at their standard path.  Note that everything defined
in urls.defaults is available here as well.

See ``urls.defaults`` for a list of all URLs available across both
configurations.
"""
from .defaults import *

urlpatterns += patterns('',

    # Examples:
    # url(r'^$', 'prod/{{ project_name }}.views.debug', name='debug'),
    # url(r'^prod/{{ project_name }}/', include('{{ project_name }}.debug.urls')),
)
