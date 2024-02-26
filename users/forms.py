from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        filter_result = User.objects.filter(username__exact = username)
        if not filter_result:
            raise forms.ValidationError('用户不存在.')

        return username