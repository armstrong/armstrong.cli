from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Below is an example well view that might be used to display a well named
    # 'front_page' allowing for placement of content on the home page. The view
    # will work after # running `armstrong loaddata fixtures/initial_data.json`
    #
    url(r'^$', QuerySetBackedWellView.as_view(well_title='front_page',
                                              template_name="front_page.html",
                                              queryset=Article.published.all()),
        name='front_page'),
)
