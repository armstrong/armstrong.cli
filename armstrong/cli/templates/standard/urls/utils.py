from armstrong.core.arm_sections.models import Section
from armstrong.apps.articles.models import Articles
from django.core.urlresolvers import reverse

def get_url_for_model(obj):
    if obj.__class__ == Section:
        return reverse('section_view', kwargs={'full_slug': obj.full_slug})
    if obj.__class__ == Article:
        return reverse('article_detail', kwargs={'slug': obj.slug})
