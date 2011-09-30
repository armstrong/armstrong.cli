from tastypie.api import Api

from .resources import ArticleResource
from .resources import AuthorsResource

v1_api = Api(api_name="v1")
v1_api.register(ArticleResource())
v1_api.register(AuthorsResource())