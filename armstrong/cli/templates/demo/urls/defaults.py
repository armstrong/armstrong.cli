from django.conf.urls.defaults import patterns, include, url
from armstrong.core.arm_wells.views import QuerySetBackedWellView
from armstrong.core.arm_sections.views import SimpleSectionView, SectionFeed
from armstrong.apps.articles.models import Article
from armstrong.apps.articles.views import ArticleFeed
from django.views.generic.list_detail import object_detail
from django.conf import settings


# ADMIN_BASE is the base URL for your Armstrong admin.  It is highly
# recommended that you change this to a different URL unless you enforce a
# strict password-strength policy for your users.
ADMIN_BASE = "admin"


# Comment the next two lines out to disable the admin:
from armstrong import hatband as admin
admin.autodiscover()

# TODO: Document why this is here
from .utils import get_url_for_model

urlpatterns = patterns('',
    # Examples:
    #
    #     url(r'^$', '{{ project_name }}.views.home', name='home'),
    #     url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # ## Django Admin
    # Comment the admin/doc line below to disable admin documentation:
    url(r'^%s/doc/' % ADMIN_BASE, include('django.contrib.admindocs.urls')),

    # Comment the next line to disable the admin:
    url(r'^%s/' % ADMIN_BASE, include(admin.site.urls)),

    # ## Media serving
    #
    # Configure the basic Django media view to respond to requests.
    #
    # *Note*: You should not use this in production, but it's useful to have
    # for development purposes.
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),

    # ## Front Page
    #
    # This is an example of a `QuerySetBackedWellView` for loading articles
    # while using a well called `front_page`.  `QuerySetBackedWellView`
    # requires a well to exist by default, but this is configured to work
    # even without a well because of the `allow_empty=True` kwarg.
    url(r'^$',
            QuerySetBackedWellView.as_view(well_title="front_page",
                    allow_empty=True, template_name="index.html",
                    queryset=Article.published.all()),
            name="home"),

    # ## Section Views
    #
    # Generate a section page.  Note that it grabs a forward slash
    # (/) as well since it matches on the full slug.
    url(r'^section/(?P<full_slug>[-\w/]+)',
            SimpleSectionView.as_view(template_name='section.html'),
            name='section_view'),

    # Generate a basic RSS/Atom feed for any Section page.  Like the
    # default Section view, this also grabs forward slashes as well.
    url(r'^feed/section/(?P<full_slug>[-\w/]+)',
            SectionFeed(section_view='section_view'),
            name='section_feed'),

    # ## Article Views
    #
    # Generate a detail view for a given article
    url(r'^article/(?P<slug>[-\w]+)/', object_detail, {
                'queryset': Article.published.all().select_subclasses(),
                'template_name': 'article.html',
                'slug_field': 'slug',
            },
            name='article_detail'),

    # Generate a basic RSS/Atom feed for all articles
    url(r'^feed/all',
            ArticleFeed(title='Demo site articles',
                        link='/',
                        queryset=Article.objects.all()),
            name='all_articles_feed'),

)

# ## API Routes
#
# Armstrong ships with a basic API.  You can uncomment the following two
# lines (and adjust indention) to enable it.
#
#     from .api import urlpatterns as api_urlpatterns
#     urlpatterns += api_urlpatterns
