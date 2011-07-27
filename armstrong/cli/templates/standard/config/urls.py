from django.conf.urls.defaults import patterns, include, url
from armstrong.core.arm_wells.views import QuerySetBackedWellView
from armstrong.core.arm_sections.views import SimpleSectionView
from armstrong.apps.articles.models import Article
from django.views.generic.list_detail import object_detail
# ADMIN_BASE is the base URL for your Armstrong admin.  It is highly
# recommended that you change this to a different URL unless you enforce a
# strict password-strength policy for your users.
ADMIN_BASE = "admin"


# Comment the next two lines out to disnable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', '{{ project_name }}.views.home', name='home'),
    # url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Comment the admin/doc line below to disable admin documentation:
    url(r'^%s/doc/' % ADMIN_BASE, include('django.contrib.admindocs.urls')),

    # Comment the next line to disable the admin:
    url(r'^%s/' % ADMIN_BASE, include(admin.site.urls)),

    # {% if demo %}
    url(r'^$', QuerySetBackedWellView.as_view(well_title='front_page',
                                              template_name="front_page.html",
                                              queryset=Article.published.all()),
            name='front_page'),
    # {% else %}
    # Below is an example well view that might be used to display a well named
    # 'front_page' allowing for placement of content on the home page. The view
    # will work after # running `armstrong loaddata fixtures/initial_data.json`
    #
    #url(r'^$', QuerySetBackedWellView.as_view(well_title='front_page',
    #                                          template_name="front_page.html",
    #                                          queryset=Article.published.all()),
    #        name='front_page'),
    #
    # Load the Armstrong "success" page by default
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    # {% endif %}

    url(r'^section/(?P<full_slug>[-\w/]+)', 
            SimpleSectionView.as_view(template_name='section.html'),
            name='section_view'),

    url(r'^article/(?P<slug>[-\w]+)/', object_detail, {
                        'queryset':Article.published.all().select_subclasses(),
                        'template_name':'article.html',
                        'slug_field':'slug',
                    },
            name='article_detail'),
)
