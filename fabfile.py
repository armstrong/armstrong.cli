from fabric.api import *
from armstrong.dev.tasks import test

full_name = "armstrong.cli"


@task
def reinstall():
    local("pip uninstall -y `basename \`pwd\`` ; pip install .")


@task
def generate_images():
    import os
    import sys
    sys.path.insert(0, os.getcwd())
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings.development"

    import Image
    import ImageDraw
    import random
    from armstrong.apps.images import models
    from armstrong.apps.articles.models import Article
    from armstrong.apps.related_content.models import RelatedContent, RelatedType
    import datetime
    from django.core.files import File
    from django.conf import settings

    WIDTH = 640
    HEIGHT = 480

    def rint(x):
        return random.randint(1, x)

    def getRandomPt():
        return (rint(WIDTH - 1), rint(HEIGHT - 1))

    def getRandomColor():
        return (rint(255), rint(255), rint(255))

    def make_image(path):
        im = Image.new('RGB', (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(im)
        for j in range(20):
            draw.rectangle((getRandomPt(), getRandomPt()), fill=getRandomColor())
        del draw
        with open(path, 'wb') as f:
            im.save(f)

    lede_art, created = RelatedType.objects.get_or_create(title='lede_art')

    for i, article in enumerate(Article.objects.all()):
        image_path = '/tmp/images/image-%i.png' % i
        make_image(image_path)
        img = models.Image.objects.create(title='image-%i' % i,
                                          slug='image-%i' % i,
                                          summary='colored boxes',
                                          pub_status='P',
                                          pub_date=datetime.datetime.now(),
                                          image=File(open(image_path)))
        img.sites.add(settings.SITE_ID)
        RelatedContent.objects.create(destination_object=img,
                                      source_object=article,
                                      related_type=lede_art)
