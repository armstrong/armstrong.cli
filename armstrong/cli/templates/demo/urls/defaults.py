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

from .utils import get_url_for_model

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', '{{ project_name }}.views.home', name='home'),
    # url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Comment the admin/doc line below to disable admin documentation:
    url(r'^%s/doc/' % ADMIN_BASE, include('django.contrib.admindocs.urls')),

    # Comment the next line to disable the admin:
    url(r'^%s/' % ADMIN_BASE, include(admin.site.urls)),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),

    # Below is an example well view that might be used to display a well named
    # 'front_page' allowing for placement of content on the home page.  The view
    # works so long as there is a well with the title ``front_page`` present.
    url(r'^$', QuerySetBackedWellView.as_view(well_title='front_page',
                                              template_name="front_page.html",
                                              queryset=Article.published.all()),
        name='front_page'),

    url(r'^section/(?P<full_slug>[-\w/]+)',
            SimpleSectionView.as_view(template_name='section.html'),
            name='section_view'),
    url(r'^feed/section/(?P<full_slug>[-\w/]+)',
            SectionFeed(section_view='section_view'),
            name='section_feed'),

    url(r'^feed/all',
            ArticleFeed(title='Demo site articles',
                        link='/',
                        queryset=Article.objects.all()),
            name='all_articles_feed'),

    url(r'^article/(?P<slug>[-\w]+)/', object_detail, {
                        'queryset': Article.published.all().select_subclasses(),
                        'template_name': 'article.html',
                        'slug_field': 'slug',
                    },
            name='article_detail'),
)

# Uncomment the following two lines if you want to expose our default API
# from .api import urlpatterns as api_urlpatterns
# urlpatterns += api_urlpatterns
