from django import forms
import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class EditProjForm(forms.Form):
    name = forms.CharField(label='项目名*')
    envs = (
        ('prod', '生产环境'),
        ('uat', '联调环境'),
        ('test', '测试环境'),
        ('dev', '开发环境'),
    )
    env = forms.ChoiceField(choices=envs, label='环境') 
    mx_versions = (
        ('4.0', '4.0'),
        ('5.0', '5.0'),
    )
    mx_version = forms.ChoiceField(choices=mx_versions, label='大版本')
    cp_addr = forms.CharField(max_length=200, help_text='请以https://或http://开头', label='管理后台地址', required=False)
    cp_admin = forms.CharField(max_length=50, label='管理后台管理员账号', required=False)
    cp_password = forms.CharField(max_length=100, label='管理后台管理员密码', required=False)
    monitor_addr = forms.CharField(max_length=200, label='监控平台地址', required=False)
    monitor_admin = forms.CharField(max_length=50, label='监控平台账号', required=False)
    monitor_password = forms.CharField(max_length=100, label='监控平台密码', required=False)
    ops_admin = forms.CharField(max_length=50, label='运维全景图测试账号', required=False)
    ops_password = forms.CharField(max_length=100, label='运维全景图测试账号密码', required=False)
    remark = forms.CharField(widget=forms.Textarea,label='备注',required=False)

    def clean_cp_addr(self):
        if not self.cleaned_data['cp_addr'] == '':
            cp_addr = self.cleaned_data['cp_addr']
            if re.match("[http|https].*", cp_addr) is None:
                raise ValidationError(_('地址不合法'))
            return cp_addr

    def clean_monitor_addr(self):
        if not self.cleaned_data['monitor_addr'] == '':
            monitor_addr = self.cleaned_data['monitor_addr']
            if re.match("[http|https].*", monitor_addr) is None:
                raise ValidationError(_('地址不合法'))
            return monitor_addr

class EditServerForm(forms.Form):
    project = forms.CharField(label='所属项目')
    env = forms.CharField(label='环境')
    ip = forms.CharField(label='服务器IP*')
    root = forms.CharField(label='服务器账号', help_text='"/"分隔多个', required=False)
    passwd = forms.CharField(label='服务器密码', help_text='"/"分隔多个', required=False)
    remote_port = forms.IntegerField(label='远程端口', required=False)
    cpu = forms.IntegerField(label='cpu核数', required=False)
    mem = forms.IntegerField(label='内存大小(G)', required=False)
    disk = forms.IntegerField(label='磁盘大小(G)', required=False)
    os_types = (
        ('l','linux'),
        ('w','windows'),
    )
    os_type = forms.ChoiceField(choices=os_types,label='系统类型')
    os = forms.CharField(label='系统版本', required=False)
    remark = forms.CharField(widget=forms.Textarea,label='备注',required=False)

    #设置ip,项目和环境为只读
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args,**kwargs)
        #self.fields['ip'].widget.attrs['readonly'] = True
        self.fields['project'].widget.attrs['readonly'] = True
        self.fields['env'].widget.attrs['readonly'] = True

class EditServiceForm(forms.Form):
    project = forms.CharField(label='项目名*')
    env = forms.CharField(label='环境')
    server = forms.CharField(label='所在服务器', required=False)
    name = forms.CharField(label='应用名*')
    service_version = forms.CharField(label='应用版本号', required=False)
    protocol_port = forms.CharField(label='协议-端口', help_text='"/"分隔多个', required=False)
    db_root = forms.CharField(label='数据库账号', required=False)
    db_passwd = forms.CharField(label='数据库密码', required=False)
    charcaters = (
        ('S', '单节点'),
        ('M', '主节点'),
        ('SA', '从节点'),
        ('A', '仲裁'),
        ('DU', '双节点'),
    )
    charcater = forms.ChoiceField(choices=charcaters,label='应用角色', required=False)
    repl_name = forms.CharField(label='集群名', required=False)
    remark = forms.CharField(widget=forms.Textarea, label='备注', required=False)

    #设置应用名,项目,环境和应用名为只读
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args,**kwargs)
        self.fields['project'].widget.attrs['readonly'] = True
        self.fields['env'].widget.attrs['readonly'] = True
        self.fields['server'].widget.attrs['readonly'] = True
        #self.fields['name'].widget.attrs['readonly'] = True

class AddProjForm(EditProjForm):
    envs = (
        ('prod', '生产环境'),
        ('uat', '联调环境'),
        ('test', '测试环境'),
        ('dev', '开发环境'),
    )
    env = forms.ChoiceField(choices=envs, label='环境')

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args,**kwargs)
        self.fields['name'].widget.attrs['readonly'] = False
        self.fields['env'].widget.attrs['readonly'] = False

class AddServerForm(EditServerForm):

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args,**kwargs)
        self.fields['ip'].widget.attrs['readonly'] = False
        self.fields['project'].widget.attrs['readonly'] = True
        self.fields['env'].widget.attrs['readonly'] = True

class AddServiceForm(EditServiceForm):

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args,**kwargs)
        self.fields['project'].widget.attrs['readonly'] = True
        self.fields['env'].widget.attrs['readonly'] = True
        self.fields['server'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = False

