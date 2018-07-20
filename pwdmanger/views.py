# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

from .models import Passwd_info
from .forms import Passwd_infoForm

import datetime
from django.db.models import Count, Min, Sum

# for limits
from django.contrib.auth.decorators import login_required, permission_required


@login_required()
def index(request):
    app_info = get_apps_info()
    order_info = get_order_info()
    cluster_info = get_cluster_info()
    os_info=get_os_info()
    owners = Passwd_info.objects.values('order').distinct()
    apps = Passwd_info.objects.values('apps').distinct()
    ops = Passwd_info.objects.values('op').distinct()
    cluster = Passwd_info.objects.values('cluster_name').distinct()
    content = {'order': owners, 'apps': apps, 'ops': ops, 'cluster': cluster, 'app_info': app_info,
               'order_info': order_info, 'cluster_info': cluster_info,'os_info':os_info}
    return render(request, 'pwdmanger/index.html', content)


def test(request):
    return render(request, 'pwdmanger/list.html')


@permission_required('pwdmanger.delete_passwd_info', 'pwdmanger.add_passwd_info', 'pwdmanger.change_passwd_info')
@login_required()
def passwd_list(request):
    pwd_list = Passwd_info.objects.all().order_by('changed_time')
    content = {'pwd_list': pwd_list}
    return render(request, 'pwdmanger/list.html', content)


@permission_required('pwdmanger.delete_passwd_info', 'pwdmanger.add_passwd_info', 'pwdmanger.change_passwd_info')
@login_required()
def passwd_edit(request, item_id):
    entry = Passwd_info.objects.get(id=item_id)

    if request.method != 'POST':
        form = Passwd_infoForm(instance=entry)
    else:
        form = Passwd_infoForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pwdmanger:passwd_list'))
    content = {'entry': entry, 'form': form}
    return render(request, 'pwdmanger/edit.html', content)


@permission_required('pwdmanger.delete_passwd_info', 'pwdmanger.add_passwd_info', 'pwdmanger.change_passwd_info')
@login_required()
def passwd_add(request):
    if request.method != 'POST':
        form = Passwd_infoForm()
    else:
        form = Passwd_infoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pwdmanger:passwd_list'))
    content = {'form': form}
    return render(request, 'pwdmanger/add.html', content)


@permission_required('pwdmanger.delete_passwd_info', 'pwdmanger.add_passwd_info', 'pwdmanger.change_passwd_info')
@login_required()
def passwd_delete(request, item_id):
    Passwd_info.objects.get(id=item_id).delete()
    return HttpResponseRedirect(reverse('pwdmanger:passwd_list'))


#
# def get_month():
#     year_month=[]
#     year=int(datetime.datetime.now().strftime("%Y"))
#     year_month=[datetime.date(year,m,1).strftime('%Y-%m') for m in range(1,13)]
#
#     data_list=[]
#     for i in year_month:
#         _tmp=Passwd_info.objects.filter(created_time=)
#         data_list.append(_tmp)
#
#     return year_month,data_list

def get_apps_info():
    apps_info = Passwd_info.objects.values_list('apps').annotate(Count('id'))
    data = []
    x = '应用'
    y = '数量'
    for i in apps_info:
        list_data = list(i)
        _tmp_data = {x: list_data[0], y: list_data[1]}
        data.append(_tmp_data)
    return data


def get_order_info():
    order_info = Passwd_info.objects.values_list('order').annotate(Count('id'))
    data = []
    x = '负责人'
    y = '数量'
    for i in order_info:
        list_data = list(i)
        _tmp_data = {x: list_data[0], y: list_data[1]}
        data.append(_tmp_data)
    return data


def get_cluster_info():
    cluster_info = Passwd_info.objects.values_list('cluster_name').annotate(Count('id'))
    data = []
    x = 'label'
    y = 'value'
    for i in cluster_info:
        list_data = list(i)
        _tmp_data = {x: list_data[0], y: list_data[1]}
        data.append(_tmp_data)
    return data

def get_os_info():
    os_info = Passwd_info.objects.values_list('os_type').annotate(Count('id'))
    data = []
    x = 'label'
    y = 'value'
    for i in os_info:
        list_data = list(i)
        _tmp_data = {x: list_data[0], y: list_data[1]}
        data.append(_tmp_data)
    return data
