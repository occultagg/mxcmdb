from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from .forms import LoginForm

# Create your views here.

def login(request):
    if request.method != 'POST':
        form = LoginForm()
        redirect_to = request.GET['next']
        context = {
            'form': form,
            'redirect_to': redirect_to,
        }
        return render(request, 'users/login.html', context=context)
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                if request.GET['next']:
                    next = request.GET['next']
                else:
                    next = '/'
                return HttpResponseRedirect(next)
            else:
                context = {
                    'form': form,
                    'message': '登录失败,请确认用户名密码.'
                }
                return render(request, 'users/login.html', context=context)
        context = {
            'form': form,
        }
        return render(request, 'users/login.html', context=context)



def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('cmdb:index'))
