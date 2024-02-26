from django.shortcuts import render, get_object_or_404
from .models import Project, Server, Permission, Service
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import EditProjForm, EditServerForm, EditServiceForm, AddProjForm, AddServerForm, AddServiceForm
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages


def index(request):
    super_users = User.objects.filter(is_superuser=True)
    init_proj, _ = Project.objects.get_or_create(name='运维', env='prod', cp_addr='内建项目,访问主页时不存在即会自动创建')
    for super_user in super_users:
        permission, _ = Permission.objects.get_or_create(user_name_id=super_user.id)
        permission.allow_projs.add(init_proj)
    return render(request, 'cmdb/index.html', context={'ops_pk': init_proj.pk})

def judge_superuser(request):
    super_users = User.objects.filter(is_superuser=True)
    current_user = request.user

    if current_user in super_users:
        return True
    else:
        return False

def url_security(request, pk):
    if not judge_superuser(request):
        current_user = request.user
        permission = Permission.objects.get(user_name=current_user)
        allow_proj_id = []
        print(allow_proj_id)
        for proj in permission.allow_projs.all():
            proj_name = str(proj).split('-')[0]
            envs = {'生产环境': 'prod', '测试环境': 'test', '联调环境': 'uat', '开发环境': 'dev'}
            proj_env = envs[str(proj).split('-')[1]]
            allow_proj_id.append(Project.objects.get(name=proj_name,env=proj_env).pk)
        if pk in allow_proj_id:
            return True
        else:
            return False
    return True

@login_required
def get_proj(request):
    global is_superuser
    is_superuser = judge_superuser(request)
    current_user = request.user

    if is_superuser:
        projs = Project.objects.filter(~Q(name='运维'))
    else:
        try:
            permission = Permission.objects.get(user_name=current_user)
        except:
            context = {'error': "你还没有授权项目,请联系管理员授权"}
            return render(request, 'cmdb/get_proj.html', context=context)

        projs = permission.allow_projs

    ops_pk = Project.objects.get(name='运维').pk

    context = {
        'projs': projs,
        'is_superuser' : is_superuser,
        'ops_pk': ops_pk,
    }
    return render(request, 'cmdb/get_proj.html', context=context)

@login_required
def proj_detail(request, pk):
    if not url_security(request, pk):
        return HttpResponse("Nice try, but not good enough.")
    proj = get_object_or_404(Project, pk=pk)
    servers = Server.objects.filter(project=pk)
    return render(request, 'cmdb/servers.html', context={
        'proj': proj,
        'servers': servers,
        'project_id': pk,
    })

@login_required
def server_detail(request, proj_pk, server_pk):
    if not url_security(request, proj_pk):
        return HttpResponse("Nice try, but not good enough.")

    server = get_object_or_404(Server, pk=server_pk, project=proj_pk)
    services = Service.objects.filter(server=server_pk)
    _ = str(server.project)
    proj = _.split('-')[0]
    env = _.split('-')[1]

    return render(request, 'cmdb/detail.html', context={
        'server': server,
        'services': services,
        'proj': proj,
        'env': env,
        'proj_pk': proj_pk,
    })

def get_form_value_or_none(value):
    if value == '':
        return None
    else:
        return value

@login_required
def edit_proj(request, pk):
    if not url_security(request, pk):
        return HttpResponse("Nice try, but not good enough.")

    proj = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = EditProjForm(request.POST)
        if form.is_valid():
            proj.name = get_form_value_or_none(form.cleaned_data['name'])
            proj.env = get_form_value_or_none(form.cleaned_data['env'])
            proj.mx_version = get_form_value_or_none(form.cleaned_data['mx_version'])
            proj.cp_addr = get_form_value_or_none(form.cleaned_data['cp_addr'])
            proj.cp_admin = get_form_value_or_none(form.cleaned_data['cp_admin'])
            proj.cp_password = get_form_value_or_none(form.cleaned_data['cp_password'])
            proj.monitor_addr = get_form_value_or_none(form.cleaned_data['monitor_addr'])
            proj.monitor_admin = get_form_value_or_none(form.cleaned_data['monitor_admin'])
            proj.monitor_password = get_form_value_or_none(form.cleaned_data['monitor_password'])
            proj.ops_admin = get_form_value_or_none(form.cleaned_data['ops_admin'])
            proj.ops_password = get_form_value_or_none(form.cleaned_data['ops_password'])
            proj.remark = get_form_value_or_none(form.cleaned_data['remark'])
            proj.save()
            return HttpResponseRedirect('/project/{}'.format(pk))
    else:
        proj_dict = model_to_dict(proj, exclude='id')
        #proj_dict['env'] = proj.get_env_display()
        form = EditProjForm(initial=proj_dict)
    context = {
        'form': form,
        'proj': proj,
    }
    return render(request, 'cmdb/edit_proj.html', context=context)

@login_required
def edit_server(request, proj_pk, server_pk):
    if not url_security(request, proj_pk):
        return HttpResponse("Nice try, but not good enough.")

    server = get_object_or_404(Server, pk=server_pk, project=proj_pk)
    if request.method == 'POST':
        form = EditServerForm(request.POST)
        if form.is_valid():
            server.ip = get_form_value_or_none(form.cleaned_data['ip'])
            server_test = Server.objects.filter(ip=form.cleaned_data['ip'],project=proj_pk)
            if server_test.exists():
                error_message = '{}-{}中{}已存在'.format(form.cleaned_data['project'], form.cleaned_data['env'], form.cleaned_data['ip'])
                form = EditServerForm(request.POST)
                context = {
                    'error_message': error_message,
                    'form': form,
                    'server': server,
                }
                return render(request, 'cmdb/edit_server.html', context=context) 
            server.root = get_form_value_or_none(form.cleaned_data['root'])
            server.passwd = get_form_value_or_none(form.cleaned_data['passwd'])
            server.remote_port = get_form_value_or_none(form.cleaned_data['remote_port'])
            server.cpu = get_form_value_or_none(form.cleaned_data['cpu'])
            server.mem = get_form_value_or_none(form.cleaned_data['mem'])
            server.disk = get_form_value_or_none(form.cleaned_data['disk'])
            server.os_type = get_form_value_or_none(form.cleaned_data['os_type'])
            server.os = get_form_value_or_none(form.cleaned_data['os'])
            server.remark = get_form_value_or_none(form.cleaned_data['remark'])
            server.save()
            return HttpResponseRedirect('/project/{}/server/{}'.format(proj_pk, server_pk))
    else:
        server_dict = model_to_dict(server, exclude='id')
        server_dict['project'] = str(server.project).split('-')[0]
        server_dict['env'] = str(server.project).split('-')[1]
        form = EditServerForm(initial=server_dict)
    context = {
        'form': form,
        'server': server,
    }
    return render(request, 'cmdb/edit_server.html', context=context)

@login_required
def edit_service(request, project_pk, server_pk, service_pk):
    if not url_security(request, project_pk):
        return HttpResponse("Nice try, but not good enough.")

    service = get_object_or_404(Service, pk=service_pk, server=server_pk)
    if request.method == 'POST':
        form = EditServiceForm(request.POST)
        if form.is_valid():
            service.name = get_form_value_or_none(form.cleaned_data['name'])
            service.service_version = get_form_value_or_none(form.cleaned_data['service_version'])
            service.protocol_port = get_form_value_or_none(form.cleaned_data['protocol_port'])
            service.db_root = get_form_value_or_none(form.cleaned_data['db_root'])
            service.db_passwd = get_form_value_or_none(form.cleaned_data['db_passwd'])
            service.repl_name = get_form_value_or_none(form.cleaned_data['repl_name'])
            service.charcater = get_form_value_or_none(form.cleaned_data['charcater'])
            service.remark = get_form_value_or_none(form.cleaned_data['remark'])
            service.save()
            return HttpResponseRedirect('/project/{}/server/{}'.format(project_pk, server_pk))
    else:
        service_dict = model_to_dict(service, exclude='id')
        service_dict['project'] = str(service.server.project).split('-')[0]
        service_dict['env'] = str(service.server.project).split('-')[1]
        service_dict['server'] = service.server.ip
        form = EditServiceForm(initial=service_dict)
    context = {
        'form': form,
        'service': service,
        'proj_pk': project_pk,
        'server_pk': server_pk,
    }
    return render(request, 'cmdb/edit_service.html', context=context)

@login_required
def proj_info(request, pk):
    if not url_security(request, pk):
        return HttpResponse("Nice try, but not good enough.")

    project = Project.objects.get(pk=pk)
    proj_name = project.name
    proj_env = project.get_env_display()
    servers = Server.objects.filter(project=project.pk)

    mysql_ip = set()
    mysql_root = set()
    mysql_passwd = set()
    mysql_port = set()
    redis_ip = set()
    redis_passwd = set()
    redis_port = set()
    mongodb_ip = set()
    mongodb_admin = set()
    mongodb_passwd = set()
    mongodb_port = set()

    for server in servers:
        services = Service.objects.filter(server=server.pk)
        for service in services:
            if service.name in ['mariadb', 'mysql']:
                mysql_ip.add(server.ip)
                mysql_root.add(service.db_root)
                mysql_passwd.add(service.db_passwd)
                mysql_port.add(service.protocol_port)
            if 'redis' in service.name or 'sentinel' in service.name:
                redis_ip.add(server.ip)
                redis_passwd.add(service.db_passwd)
                redis_port.add(service.protocol_port)
            if service.name == 'mongodb':
                mongodb_ip.add(server.ip)
                mongodb_admin.add(service.db_root)
                mongodb_passwd.add(service.db_passwd)
                mongodb_port.add(service.protocol_port)

    context = {
        'project': project,
        'proj_name': proj_name,
        'env': proj_env,
        'mysql_ip': mysql_ip,
        'mysql_root': mysql_root,
        'mysql_passwd': mysql_passwd,
        'mysql_port': mysql_port,
        'redis_ip': redis_ip,
        'redis_passwd': redis_passwd,
        'redis_port': redis_port,
        'mongodb_ip': mongodb_ip,
        'mongodb_admin': mongodb_admin,
        'mongodb_passwd': mongodb_passwd,
        'mongodb_port': mongodb_port,
    }
    return render(request, 'cmdb/proj_info.html', context=context)

@login_required
def add_proj(request):
    if request.method == "POST":
        form = AddProjForm(request.POST)
        if form.is_valid():
            proj_test = Project.objects.filter(name = form.cleaned_data['name'], env = form.cleaned_data['env'])
            if proj_test.exists():
                envs = {'prod':'生产环境', 'test': '测试环境', 'uat': '联调环境', 'dev': '开发环境'}
                error_message = '{}-{}已存在'.format(form.cleaned_data['name'], envs[form.cleaned_data['env']])
                form = AddProjForm(initial=request.POST)
                context = {
                    'error_message': error_message,
                    'form': form,
                }
                return render(request, 'cmdb/add_proj.html', context=context)

            new_proj, _ = Project.objects.get_or_create(
                name = get_form_value_or_none(form.cleaned_data['name']),
                env = get_form_value_or_none(form.cleaned_data['env']),
                mx_version = get_form_value_or_none(form.cleaned_data['mx_version']),
                cp_addr = get_form_value_or_none(form.cleaned_data['cp_addr']),
                cp_admin = get_form_value_or_none(form.cleaned_data['cp_admin']),
                cp_password = get_form_value_or_none(form.cleaned_data['cp_password']),
                monitor_addr = get_form_value_or_none(form.cleaned_data['monitor_addr']),
                monitor_admin = get_form_value_or_none(form.cleaned_data['monitor_admin']),
                monitor_password = get_form_value_or_none(form.cleaned_data['monitor_password']),
                ops_admin = get_form_value_or_none(form.cleaned_data['ops_admin']),
                ops_password = get_form_value_or_none(form.cleaned_data['ops_password']),
                remark = get_form_value_or_none(form.cleaned_data['remark']),
            )
            if not judge_superuser(request):
                current_user = request.user
                user = User.objects.get(username=current_user)
                permission, _ = Permission.objects.get_or_create(user_name=user)
                permission.allow_projs.add(new_proj.pk)
            return HttpResponseRedirect('/get_proj')
    else:
        form = AddProjForm()
    context = {
        'form': form,
    }
    return render(request, 'cmdb/add_proj.html', context=context)

@login_required
def add_server(request, pk):
    if not url_security(request, pk):
        return HttpResponse("Nice try, but not good enough.")

    project = Project.objects.get(pk=pk)

    if request.method == "POST":
        form = AddServerForm(request.POST)
        if form.is_valid():
            server_test = Server.objects.filter(ip=form.cleaned_data['ip'],project=project.pk)
            if server_test.exists():
                error_message = '{}-{}中{}已存在'.format(form.cleaned_data['project'], form.cleaned_data['env'], form.cleaned_data['ip'])
                form = AddServerForm(initial=request.POST)
                context = {
                    'error_message': error_message,
                    'form': form,
                    'project': project,
                }
                return render(request, 'cmdb/add_server.html', context=context)

            Server.objects.get_or_create(
                ip = get_form_value_or_none(form.cleaned_data['ip']),
                project = project,
                root = get_form_value_or_none(form.cleaned_data['root']),
                passwd = get_form_value_or_none(form.cleaned_data['passwd']),
                remote_port = get_form_value_or_none(form.cleaned_data['remote_port']),
                cpu = get_form_value_or_none(form.cleaned_data['cpu']),
                mem = get_form_value_or_none(form.cleaned_data['mem']),
                disk = get_form_value_or_none(form.cleaned_data['disk']),
                os_type = get_form_value_or_none(form.cleaned_data['os_type']),
                os = get_form_value_or_none(form.cleaned_data['os']),
                remark = get_form_value_or_none(form.cleaned_data['remark']),
            )
            return HttpResponseRedirect('/project/{}'.format(pk))
    else:
        init_form_data = {
            'project': project.name,
            'env': project.get_env_display(),
        }
        form = AddServerForm(initial=init_form_data)
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'cmdb/add_server.html', context=context)

@login_required
def add_service(request, proj_pk, server_pk):
    if not url_security(request, proj_pk):
        return HttpResponse("Nice try, but not good enough.")

    project = Project.objects.get(pk=proj_pk)
    server = Server.objects.get(pk=server_pk)
    if request.method == "POST":
        form = AddServiceForm(request.POST)
        if form.is_valid():
            #协议-端口重复报错
            protocol_port_list = []
            for i in Service.objects.filter(server=server):
                if not i.protocol_port is None:
                    protocol_port_list = protocol_port_list + i.protocol_port.split('/')
            if form.cleaned_data['protocol_port'] in protocol_port_list:
                error_message = '{}中{}已被占用.'.format(server.ip, form.cleaned_data['protocol_port'])
                form = AddServiceForm(initial=request.POST)
                context = {
                    'form': form,
                    'project': project,
                    'server': server,
                    'error_message': error_message,
                }
                return render(request, 'cmdb/add_service.html', context=context)

            Service.objects.get_or_create(
                name = get_form_value_or_none(form.cleaned_data['name']),
                server = server,
                service_version = get_form_value_or_none(form.cleaned_data['service_version']),
                protocol_port = get_form_value_or_none(form.cleaned_data['protocol_port']),
                db_root = get_form_value_or_none(form.cleaned_data['db_root']),
                db_passwd = get_form_value_or_none(form.cleaned_data['db_passwd']),
                repl_name = get_form_value_or_none(form.cleaned_data['repl_name']),
                charcater = get_form_value_or_none(form.cleaned_data['charcater']),
                remark = get_form_value_or_none(form.cleaned_data['remark']),
            )
            return HttpResponseRedirect('/project/{}/server/{}'.format(proj_pk, server_pk))
    else:
        init_form_data = {
            'project': project.name,
            'env': project.get_env_display(),
            'server': server.ip,
        }
        form = AddServiceForm(initial=init_form_data)
        context = {
            'form': form,
            'project': project,
            'server': server,
        }
        return render(request, 'cmdb/add_service.html', context=context)

@login_required
def del_proj(request, pk):
    if not url_security(request, pk):
        return HttpResponse("Nice try, but not good enough.")

    try:
        Project.objects.get(pk=pk).delete()
        messages.error(request, '删除成功.')
    except:
        messages.error(request, '删除失败.')
    return HttpResponseRedirect('/get_proj')

@login_required
def del_server(request, server_pk, proj_pk):
    if not url_security(request, proj_pk):
        return HttpResponse("Nice try, but not good enough.")
    try:
        Server.objects.get(pk=server_pk).delete()
        messages.error(request, '删除成功.')
    except:
        messages.error(request, '删除失败.')
    return HttpResponseRedirect('/project/{}'.format(proj_pk))

@login_required
def del_service(request, service_pk, server_pk, proj_pk):
    if not url_security(request, proj_pk):
        return HttpResponse("Nice try, but not good enough.")
    try:
        Service.objects.get(pk=service_pk).delete()
        messages.error(request, '删除成功.')
    except:
        messages.error(request, '删除失败.')
    return HttpResponseRedirect('/project/{}/server/{}'.format(proj_pk, server_pk))

