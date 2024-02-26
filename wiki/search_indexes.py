from haystack import indexes
from cmdb.models import Project
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        proj = Project.objects.get(name='运维')
        allow_projs = [Post.objects.filter(project=proj.pk)]
        return self.get_model().objects.all()
