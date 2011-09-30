from armstrong.core.arm_sections.models import Section
from armstrong.apps.articles.models import Article
from django.core.urlresolvers import reverse

def get_url_for_model(obj):
    """ The get_url_for_model function is necessary because Armstrong has no
    preconceptions about what your url schema actually looks like.
    get_url_for_model is called whenever a BaseContent subclass has it's
    get_absolute_url function calle_url_for_model is called whenever a
    BaseContent subclass has it's get_absolute_url function called.

    In the future we will most likely provide base urls for each app that will
    allow new Armstrong implementations to not use this mechanism.
    """
    if obj.__class__ == Section:
        return reverse('section_view', kwargs={'full_slug': obj.full_slug})
    if obj.__class__ == Article:
        return reverse('article_detail', kwargs={'slug': obj.slug})
