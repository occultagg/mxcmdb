from django.urls import path
from . import views

app_name = 'cmdb'
urlpatterns = [
    path('', views.index, name='index'),
    #查
    path('get_proj', views.get_proj, name='get_proj'),
    path('project/<int:pk>', views.proj_detail, name='proj_detail'),
    path('project/<int:pk>/info', views.proj_info, name='proj_info'),
    path('project/<int:proj_pk>/server/<int:server_pk>', views.server_detail, name='server_detail'),
    #增
    path('add_proj', views.add_proj, name='add_proj'),
    path('project/<int:pk>/add_server', views.add_server, name='add_server'),
    path('project/<int:proj_pk>/server/<int:server_pk>/add_service', views.add_service, name='add_service'),
    #改
    path('project/<int:pk>/edit', views.edit_proj, name='edit_proj'),
    path('project/<int:proj_pk>/server/<int:server_pk>/edit', views.edit_server, name='edit_server'),
    path('project/<int:project_pk>/server/<int:server_pk>/service/<int:service_pk>/edit', views.edit_service,
         name='edit_service'),
    #删
    path('project/<int:pk>/del', views.del_proj, name='del_proj'),
    path('server/<int:server_pk>/del?proj_pk=<int:proj_pk>', views.del_server, name='del_server'),
    path('service/<int:service_pk>/del?proj_pk=<int:proj_pk>,server_pk=<int:server_pk>', views.del_service, name='del_service'),
]