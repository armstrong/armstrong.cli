from armstrong.apps.articles.models import Article
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource


class AuthorsResource(ModelResource):
    class Meta:
        queryset = User.objects.filter(groups__name="Authors")
        resource_name = "users/author"
        excludes = ["email", "is_superuser", "password", ]


class ArticleResource(ModelResource):
    authors = fields.ToManyField(AuthorsResource, "authors")

    class Meta:
        queryset = Article.published.all()
        resource_name = "articles/article"