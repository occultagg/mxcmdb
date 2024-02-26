from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm
from cmdb.models import Project, Permission
from django.contrib.auth.decorators import login_required
from django.utils.functional import keep_lazy_text
from markdown.extensions.toc import TocExtension
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from cmdb.views import judge_superuser, url_security
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from pure_pagination import Paginator
import re
import unicodedata
import markdown
import copy

@login_required
def get_wiki(request, proj_pk=None):
    project = Project.objects.get(name='运维')
    can_modi = False
    if proj_pk is None or proj_pk == project.pk:
        proj_pk = project.pk
        top_post_list = Post.objects.filter(category='ops', is_top=True)
        post_list = Post.objects.filter(category='ops', is_top=False)
        is_ops = True
        if judge_superuser(request):
            can_modi = True
    else:
        project = Project.objects.get(pk=proj_pk)
        top_post_list = Post.objects.filter(project=proj_pk, is_top=True)
        post_list = Post.objects.filter(project=proj_pk, is_top=False)
        is_ops = False
        if url_security(request, proj_pk):
            can_modi = True
        else:
            return HttpResponse("Nice try, but not good enough.")

    result_post_list = list(top_post_list) + list(post_list)
    #分页
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    objects = result_post_list

    p = Paginator(objects, request=request, per_page=10)
    page_obj = p.page(page)

    context = {
        'proj_pk': proj_pk,
        'page_obj': page_obj,
        'is_ops': is_ops,
        'can_modi': can_modi,
        'project': project,
    }
    return render(request, 'wiki/post_list.html', context=context)

#from django.utils.text import slugify 重写该方法,让自动生生成的目录不自动小写
@keep_lazy_text
def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip()
    return re.sub(r'[-\s]+', '-', value)

@login_required
def post_detail(request, proj_pk, post_pk):
    project = Project.objects.get(name='运维')
#    if not proj_pk == project.pk:
#        if not url_security(request, proj_pk):
#            return HttpResponse("Nice try, but not good enough.")

    post = get_object_or_404(Post, pk=post_pk)

    #复制文章内容用于生成目录
    md = markdown.Markdown(extensions=[
                         'markdown.extensions.extra',
                         'markdown.extensions.codehilite',
                         TocExtension(slugify=slugify),
                         ])
    #剔除代码块内容以免代码块内备注识别为标题
    code_pattern = re.compile(r'```(?:.|\s)*?```')
    new_content = ''.join(re.split(code_pattern, post.content))

    copy_post = copy.deepcopy(post)
    copy_post.content = md.convert(new_content)

    copy_post.toc = md.toc

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    copy_post.toc = m.group(1) if m is not None else ''

    #print(copy_post.toc)

    can_modi = False
    if post.project == Project.objects.get(name='运维'):
        is_ops = True
        if judge_superuser(request):
            can_modi = True
    else:
        is_ops = False
        if request.user == post.author or judge_superuser(request):
            can_modi = True

    context = {
        'post': post,
        'copy_post': copy_post,
        'proj_pk': proj_pk,
        'is_ops': is_ops,
        'can_modi': can_modi,
    }
    return render(request, 'wiki/post.html', context=context)

@login_required
def post_add_edit(request, proj_pk, post_pk=None):
    if not url_security(request, proj_pk):
        return HttpResponse("Nice try, but not good enough.")

    project = Project.objects.get(pk=proj_pk)
    author = request.user
    ops_proj = Project.objects.get(name='运维')
    if ops_proj.pk == proj_pk:
        category = '运维文档'
    else:
        category = '项目文档'

    init_form_data = {
        'project': '{}-{}'.format(project.name, project.get_env_display()),
        'author': author,
        'category': category,
    }
    #提交
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data['author'])

            categorys = {
                '运维文档': 'ops',
                '项目文档': 'proj',
            }
            #编辑提交
            #print(post_pk)
            if not post_pk == None:
                post = Post.objects.get(pk=post_pk)
                post.title = form.cleaned_data['title']
                post.is_top = form.cleaned_data['is_top']
                post.author = user
                post.project = project
                post.content = form.cleaned_data['content']
                #post.excerpt = form.cleaned_data['excerpt']
                post.save()
                return HttpResponseRedirect(reverse('wiki:post_detail', args=[proj_pk, post_pk]))
            #新增提交
            else:
                new_post, _ = Post.objects.get_or_create(
                    title = form.cleaned_data['title'],
                    is_top = form.cleaned_data['is_top'],
                    author = user,
                    category = categorys[form.cleaned_data['category']],
                    project = project,
                    content = form.cleaned_data['content'],
                    #excerpt = form.cleaned_data['excerpt'],
                )
            if form.cleaned_data['category'] == '运维文档':
                return HttpResponseRedirect(reverse('wiki:get_ops_wiki'))
            elif form.cleaned_data['category'] == '项目文档':
                return HttpResponseRedirect(reverse('wiki:get_wiki', args=[proj_pk]))
    #编辑get
    elif not post_pk == None:
        init_form_data['is_top'] = Post.objects.get(pk=post_pk).is_top
        init_form_data['content'] = Post.objects.get(pk=post_pk).content
        init_form_data['title'] = Post.objects.get(pk=post_pk).title
        init_form_data['excerpt'] = Post.objects.get(pk=post_pk).excerpt
        form = PostForm(initial=init_form_data)
        context = {
            'project': project,
            'form': form,
            'is_edit': True,
            'post_pk': post_pk,
        }
        return render(request, 'wiki/add_edit_post.html', context=context)
    #新增get
    else:
        form = PostForm(initial=init_form_data)
        context = {
            'project': project,
            'form': form,
        }
        return render(request, 'wiki/add_edit_post.html', context=context)

@login_required
def del_post(request, proj_pk, post_pk):
    if not url_security(request, proj_pk):
        return HttpResponse("Nice try, but not good enough.")
    try:
        Post.objects.get(pk=post_pk).delete()
        messages.error(request, '删除成功.')
    except:
        messages.error(request, '删除失败.')
    if proj_pk == Project.objects.get(name='运维').pk:
        return HttpResponseRedirect(reverse('wiki:get_ops_wiki'))
    else:
        return HttpResponseRedirect(reverse('wiki:get_wiki', args=[proj_pk]))

from haystack.query import SearchQuerySet, SQ
from haystack.generic_views import SearchView
from cmdb.models import Permission, Project
from cmdb.views import judge_superuser

class MySearchView(SearchView):
    template_name = "wiki/search.html"

    def get_queryset(self):
        queryset = super(MySearchView, self).get_queryset()
        if judge_superuser(self.request):
            return queryset
        else:
            username = self.request.user
            try:
                permission = Permission.objects.get(user_name=username)
            except:
                context['error_message'] = '该用户还没有授权项目,请联系管理员.'
                return queryset
            ops_proj = Project.objects.get(name='运维')
            allow_projs = [i for i in permission.allow_projs.all()]
            allow_projs.append(ops_proj)
            q = queryset.filter(project__in=allow_projs)
            print(dir(q))
            print(q.models)
            return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
#        if judge_superuser(self.request):
#            return context
#        else:
#            username = self.request.user
#            try:
#                permission = Permission.objects.get(user_name=username)
#            except:
#                context['error_message'] = '该用户还没有授权项目,请联系管理员.'
#                return context
#            ops_proj = Project.objects.get(name='运维')
#            allow_projs = [i for i in permission.allow_projs.all()]
#            allow_projs.append(ops_proj)
#            #allow_posts = Post.objects.filter(project__in=allow_projs)
#            #context['object_list'] = allow_posts
#            for i in context['page_obj'].__dict__['object_list']:
#                if not i.object.project in allow_projs:
#                    context['page_obj'].__dict__['object_list'].remove(i)
#            print(context['page_obj'].__dict__['object_list'])
        return context
