from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

#项目
class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name='项目名')
    #不同环境有不同的后台地址和账号密码,因此env必须放在project
    envs = (
        ('prod','生产环境'),
        ('uat','联调环境'),
        ('dev', '开发环境'),
        ('test','测试环境'),
    )
    env = models.CharField(max_length=100, choices=envs, default='pord', blank=False, verbose_name='环境')

    mx_versions = (
        ('4.0', '4.0'),
        ('5.0', '5.0'),
    )

    mx_version = models.CharField(max_length=8, choices=mx_versions, help_text='大版本', null=True, blank=True, verbose_name='大版本')
    cp_addr = models.CharField(max_length=200, help_text='请以https://或http://开头', null=True, blank=True, verbose_name='管理后台地址')
    cp_admin = models.CharField(max_length=50, verbose_name='管理后台管理员账号', null=True, blank=True, default='admin')
    cp_password = models.CharField(max_length=100, verbose_name='管理后台管理员密码', null=True, blank=True, default='12345678')
    monitor_addr = models.CharField(max_length=200, verbose_name='监控平台地址', null=True, blank=True)
    monitor_admin = models.CharField(max_length=50, verbose_name='监控平台账号', null=True, blank=True, default='admin')
    monitor_password = models.CharField(max_length=100, verbose_name='监控平台密码', null=True, blank=True, default='MeiXin@2020')
    ops_admin = models.CharField(max_length=50, verbose_name='运维全景图测试账号', null=True, blank=True)
    ops_password = models.CharField(max_length=100, verbose_name='运维全景图测试账号密码', null=True, blank=True)
    remark = models.TextField(max_length=400, verbose_name='备注', blank=True, null=True)

    def __str__(self):
        return self.name + '-' + self.get_env_display()

    def get_absolute_url(self):
        return reverse('cmdb:proj_detail', kwargs={'pk': self.pk})

class Permission(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE, help_text='注意:选超级管理员的话,配置不生效')
    allow_projs = models.ManyToManyField(Project)

    def __str__(self):
        return str(self.user_name)

#服务器
class Server(models.Model):
    ip = models.GenericIPAddressField(verbose_name='服务器ip', blank=False, default='1.1.1.1')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, verbose_name='关联项目')

    root = models.CharField(max_length=200, blank=True, null=True, default='root', verbose_name='服务器账号')
    passwd = models.CharField(max_length=400, blank=True, verbose_name='服务器密码', null=True)
    remote_port = models.IntegerField(blank=True, default=22, verbose_name='远程端口', help_text='22,3389等', null=True)
    cpu = models.IntegerField(verbose_name='CPU核数', blank=True, null=True)
    mem = models.IntegerField(verbose_name='内存,单位G', blank=True, null=True)
    disk = models.IntegerField(verbose_name='磁盘,单位G', blank=True, null=True)
    os = models.CharField(max_length=50, verbose_name='系统版本', help_text='如centos7;windows server 2016等', blank=True, null=True)

    mac = models.CharField(max_length=50, blank=True, verbose_name='物理地址', null=True)

    os_types = (
        ('l','linux'),
        ('w','windows'),
    )

    os_type = models.CharField(max_length=50, choices=os_types, default='l', blank=False, verbose_name='系统类型')

    remark = models.TextField(max_length=400, verbose_name='备注', blank=True, null=True)

    def __str__(self):
        return str(self.project) + '-' + str(self.ip)

    def get_absolute_url(self):
        return reverse('cmdb:server_detail', kwargs={'server_pk': self.pk, 'proj_pk': self.project.pk})

    def project_name(self):
        return self.project.name

    def project_env(self):
        return self.project.get_env_display()

#服务
class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='应用名', help_text='mx-base,mx-apps,ima,msg,zk,es,etc...')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, blank=False, null=True, verbose_name='关联服务器')
    protocol_port = models.CharField(
        max_length=100, verbose_name='协议-端口',
        help_text='请输入协议和端口,"-"连接,例如"TCP-8080",多个协议端口请用"/"分割',
        blank=True, null=True)
    db_root = models.CharField(max_length=100, verbose_name='数据库账号', help_text='数据库才需要填写,多个账号请用"/"分隔', blank=True, null=True)
    db_passwd = models.CharField(max_length=100, verbose_name='数据库密码', help_text='与数据库账号一一对应,请用"/"分隔', blank=True, null=True)
    service_version = models.CharField(max_length=30, verbose_name='应用版本号', blank=True, null=True)

    charcaters = (
        ('S', '单节点'),
        ('M', '主节点'),
        ('SA', '从节点'),
        ('A', '仲裁'),
        ('DU', '双节点'),
    )
    charcater = models.CharField(max_length=50, choices=charcaters, verbose_name='节点角色', default='S', blank=True, null=True)
    repl_name = models.CharField(max_length=100, verbose_name='集群名', blank=True, null=True)
    remark = models.TextField(max_length=400, verbose_name='备注', help_text='可用于注明定制模块功能或其他信息', blank=True, null=True)

    def __str__(self):
        return self.name

    def server_project(self):
        return self.server.project.name

    def server_env(self):
        return self.server.project.get_env_display()

    def server_ip(self):
        return self.server.ip

    def get_absolute_url(self):
        return reverse('cmdb:edit_service', kwargs={'service_pk': self.pk, 'project_pk': self.server.project.pk, 'server_pk': self.server.pk})






