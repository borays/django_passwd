from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:user_login'))


def user_register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        print(form)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('pwdmanger:passwd_list'))
    content = {'form': form}
    return render(request, 'users/register.html', content)


def user_change_pass(request):
    if request.method!='POST':
        form=PasswordChangeForm(request.user.username)
    else:
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            logout(request)
            return HttpResponseRedirect(reverse('users:user_login'))
    content={'form':form}
    return render(request, 'users/change.html', content)