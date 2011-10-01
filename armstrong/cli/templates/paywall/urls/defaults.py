from django.conf.urls.defaults import patterns, include, url
from armstrong.core.arm_wells.views import QuerySetBackedWellView
from armstrong.core.arm_sections.views import SimpleSectionView, SectionFeed
from armstrong.core.arm_access.paywalls.subscription import SubscriptionPaywall
from armstrong.core.arm_access.paywalls import render_on_deny
from armstrong.apps.articles.models import Article
from armstrong.apps.articles.views import ArticleFeed
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
# ADMIN_BASE is the base URL for your Armstrong admin.  It is highly
# recommended that you change this to a different URL unless you enforce a
# strict password-strength policy for your users.
ADMIN_BASE = "admin"


# Comment the next two lines out to disable the admin:
from armstrong import hatband as admin
admin.autodiscover()

paywall = SubscriptionPaywall(permission_denied=render_on_deny('permission_denied.html'))

from .utils import get_url_for_model

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'baz.views.home', name='home'),
    # url(r'^baz/', include('baz.foo.urls')),

    # Comment the admin/doc line below to disable admin documentation:
    url(r'^%s/doc/' % ADMIN_BASE, include('django.contrib.admindocs.urls')),

    # Comment the next line to disable the admin:
    url(r'^%s/' % ADMIN_BASE, include(admin.site.urls)),

    url(r'^$',
            QuerySetBackedWellView.as_view(well_title='front_page',
                                           template_name="front_page.html",
                                           queryset=Article.published.all(),
                                    ),
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

    url(r'^article/(?P<slug>[-\w]+)/',
            paywall.protect(DetailView.as_view(
                                    queryset=Article.published.all(),
                                    template_name='article.html',
                                    slug_field='slug',
                                ),
                            template_object_name='object'),
            name='article_detail'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

# Uncomment the following two lines if you want to expose our default API
# from .api import urlpatterns as api_urlpatterns
# urlpatterns += api_urlpatterns
