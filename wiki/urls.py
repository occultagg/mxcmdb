from django.urls import path
from . import views

app_name = 'wiki'
urlpatterns = [
    #查
    path('ops_wiki', views.get_wiki, name='get_ops_wiki'),
    path('proj/<int:proj_pk>/wiki', views.get_wiki, name='get_wiki'),
    path('proj/<int:proj_pk>/post/<int:post_pk>', views.post_detail, name='post_detail'),
    #增
    path('proj/<int:proj_pk>/post/add', views.post_add_edit, name='post_add'),
    #改
    path('proj/<int:proj_pk>/post/<int:post_pk>/edit', views.post_add_edit, name='post_edit'),
    #删
    path('proj/<int:proj_pk>/post/<int:post_pk>/del', views.del_post, name='post_del'),
    #搜索
    path('search/', views.MySearchView.as_view(), name='search_wiki'),
]
