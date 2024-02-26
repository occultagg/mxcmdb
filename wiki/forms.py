from django import forms
from mdeditor.fields import MDTextFormField


class PostForm(forms.Form):
    title = forms.CharField(label='标题',required=True)
    is_top = forms.BooleanField(label='是否置顶', required=False)
    author = forms.CharField(label='作者')
    category = forms.CharField(label='文档类型')
    project = forms.CharField(label='项目')
    content = MDTextFormField(label='文章内容', required=True)
    #excerpt = forms.CharField(label='摘要', required=False, help_text='留空则自动生成')

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args,**kwargs)
        self.fields['author'].widget.attrs['readonly'] = True
        self.fields['category'].widget.attrs['readonly'] = True
        self.fields['project'].widget.attrs['readonly'] = True
