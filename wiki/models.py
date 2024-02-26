from django.db import models
from mdeditor.fields import MDTextField
from django.contrib.auth.models import User
from cmdb.models import Project
from django.urls import reverse
from django.utils.html import strip_tags
import markdown

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100, blank=False, verbose_name='标题')
    excerpt = models.CharField(max_length=400, blank=True, verbose_name='摘要')
    is_top = models.BooleanField(verbose_name='置顶')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    categorys = (
        ('ops', '运维文档'),
        ('proj', '项目文档'),
    )
    category = models.CharField(max_length=20, choices=categorys, verbose_name='分类')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, verbose_name='关联项目', null=True)
    content = MDTextField(verbose_name="文章")
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('wiki:post_detail', kwargs={'post_pk': self.pk, 'proj_pk': self.project.pk})

    def save(self, *args, **kwargs):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.content))[:54]
    
        super().save(*args, **kwargs)
