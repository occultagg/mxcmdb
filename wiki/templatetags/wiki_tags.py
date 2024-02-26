from ..models import Post
from cmdb.models import Project
from django import template
from django.db.models import Q

# 实例化
register = template.Library()

# 最新文章标签
# 实例化后调用方法再作为装饰器使用


@register.simple_tag
def get_ops_posts():
    return Post.objects.filter(category='ops').order_by('-created_time')

# 归档模版标签
@register.simple_tag
def archives():
    proj_list = Project.objects.filter(~Q(name='运维'))
    return proj_list

