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

# for paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# for use js data
from django.forms.models import model_to_dict

# for search
from django.db.models import Q

@permission_required('pwdmanger.delete_passwd_info', 'pwdmanger.add_passwd_info', 'pwdmanger.change_passwd_info')
@login_required()
def index(request):
    # op_info = get_op_info()
    # app_info = get_apps_info()
    order_info = get_order_info()
    cluster_info = get_cluster_info()
    os_info = get_os_info()
    owners = Passwd_info.objects.values('order').distinct()
    apps = Passwd_info.objects.values('apps').distinct()
    # ops = Passwd_info.objects.values('op').distinct()
    os_type = Passwd_info.objects.values('os_type').distinct()
    cluster = Passwd_info.objects.values('cluster_name').distinct()
    all_vm = Passwd_info.objects.all()
    # content = {'order': owners, 'apps': apps, 'ops': ops, 'cluster': cluster, 'app_info': app_info,
    #            'order_info': order_info, 'cluster_info': cluster_info, 'os_info': os_info, 'os_type': os_type,
    #            'all_vm': all_vm, 'op_info': op_info}
    content = {'order': owners, 'apps': apps, 'cluster': cluster,
               'order_info': order_info, 'cluster_info': cluster_info, 'os_info': os_info,
               'all_vm': all_vm,'os_type':os_type}
    return render(request, 'pwdmanger/index.html', content)


def test(request):
    return render(request, 'pwdmanger/list.html')


@permission_required('pwdmanger.delete_passwd_info', 'pwdmanger.add_passwd_info', 'pwdmanger.change_passwd_info')
@login_required()
def passwd_list(request):
    pwd_list = Passwd_info.objects.all().order_by('-changed_time')
    paginator = Paginator(pwd_list, 10)

    page = request.GET.get('page')
    try:
        contents = paginator.page(page)
    except PageNotAnInteger:
        contents = paginator.page(1)
    except EmptyPage:
        contents = paginator.page(paginator.num_pages)

    # data=get_list_data()
    # print(data)
    last_change = Passwd_info.objects.latest()
    # content = {'data': data, "last_change": last_change}
    content = {'pwd_list': contents, "last_change": last_change, "paginator": paginator}
    return render(request, 'pwdmanger/list.html', content)

@permission_required('pwdmanger.delete_passwd_info', 'pwdmanger.add_passwd_info', 'pwdmanger.change_passwd_info')
@login_required()
def passwd_search(request):
    q = request.GET.get('keyword')
    if not q:
        pass

    pwd_list = Passwd_info.objects.filter(
        Q(cluster_name__icontains=q) | Q(ip_address__icontains=q) | Q(host_name__icontains=q) | Q(
            user_name__icontains=q) | Q(password__icontains=q) | Q(op__icontains=q) | Q(order__icontains=q) | Q(
            os_type__icontains=q) | Q(apps__icontains=q)).order_by('-changed_time')
    nums = len(pwd_list)
    paginator = Paginator(pwd_list, 10)

    page = request.GET.get('page')
    try:
        contents = paginator.page(page)
    except PageNotAnInteger:
        contents = paginator.page(1)
    except EmptyPage:
        contents = paginator.page(paginator.num_pages)

    content = {'pwd_list': contents, "nums": nums, "paginator": paginator, 'keyword': q}
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


def get_apps_info():
    apps_info = Passwd_info.objects.values_list('apps').annotate(nums=Count('id')).order_by('-nums')
    data = []
    x = '应用'
    y = '数量'
    for i in apps_info:
        list_data = list(i)
        _tmp_data = {x: list_data[0], y: list_data[1]}
        data.append(_tmp_data)

    return data


def get_order_info():
    order_info = Passwd_info.objects.values_list('order').annotate(nums=Count('id')).order_by('-nums')
    data = []
    x = '负责人'
    y = '数量'
    for i in order_info:
        list_data = list(i)
        _tmp_data = {x: list_data[0], y: list_data[1]}
        data.append(_tmp_data)
    return data


def get_cluster_info():
    cluster_info = Passwd_info.objects.values_list('cluster_name').annotate(nums=Count('id')).order_by('-nums')
    data = []
    x = 'label'
    y = 'value'
    for i in cluster_info:
        list_data = list(i)
        _tmp_data = {x: list_data[0], y: list_data[1]}
        data.append(_tmp_data)
    return data


def get_os_info():
    os_info = Passwd_info.objects.values_list('os_type').annotate(nums=Count('id')).order_by('-nums')
    data = []
    x = 'label'
    y = 'value'
    for i in os_info:
        list_data = list(i)
        _tmp_data = {x: list_data[0], y: list_data[1]}
        data.append(_tmp_data)
    return data


def get_op_info():
    op_info = Passwd_info.objects.values_list('op').annotate(nums=Count('id')).order_by('-nums')
    data = []
    x = '运维人'
    y = '数量'
    for i in op_info:
        list_data = list(i)
        _tmp_data = {x: list_data[0], y: list_data[1]}
        data.append(_tmp_data)
    return data


@login_required()
def api_update_pass(request):
    if request.method != 'POST':
        return HttpResponse("404")
    else:
        ip = request.POST.get('ip')
        password = request.POST.get('password')
        if Passwd_info.objects.filter(ip_address=ip).update(password=password):
            return HttpResponse("OK")
        else:
            return HttpResponse("ERROR")

# def get_list_data():
#     data=[]
#     _data=Passwd_info.objects.all()
#     for i in range(_data.count()):
#         _tmp_data = list(model_to_dict(_data[i]).values())
#         data.append(_tmp_data)
#
#     return data
