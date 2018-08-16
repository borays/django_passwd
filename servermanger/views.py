from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

from .models import Server_info
from .forms import Server_infoForm

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
import json

#for messages
from django.contrib import messages

# def test(request):
#     return render(request, 'servermanger/list.html')
@login_required()
@permission_required('servermanger.delete_server_info', 'servermanger.add_server_info', 'servermanger.change_server_info')
def server_list(request):
    pwd_list = Server_info.objects.all().order_by('-changed_time')
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
    last_change = Server_info.objects.latest()
    # content = {'data': data, "last_change": last_change}
    content = {'pwd_list': contents, "last_change": last_change, "paginator": paginator}
    return render(request, 'servermanger/list.html', content)

@login_required()
@permission_required('servermanger.delete_server_info', 'servermanger.add_server_info', 'servermanger.change_server_info')
def server_edit(request, item_id):
    entry = Server_info.objects.get(id=item_id)
    flash=''

    if request.method != 'POST':
        form = Server_infoForm(instance=entry)
    else:
        form = Server_infoForm(instance=entry, data=request.POST)
        item_ip=request.POST.get('ip_address')
        if form.is_valid():
            form.save()
            messages.success(request,"数据%s修改成功！" % item_ip)
            return HttpResponseRedirect(reverse('servermanger:server_list'))
    content = {'entry': entry, 'form': form}
    return render(request, 'servermanger/edit.html', content)

@login_required()
@permission_required('servermanger.delete_server_info', 'servermanger.add_server_info', 'servermanger.change_server_info')
def server_delete(request, item_id):
    item_ip=Server_info.objects.get(id=item_id)
    Server_info.objects.get(id=item_id).delete()
    messages.success(request, "数据%s删除成功！" % item_ip)
    return HttpResponseRedirect(reverse('servermanger:server_list'))

@login_required()
@permission_required('servermanger.delete_server_info', 'servermanger.add_server_info', 'servermanger.change_server_info')
def server_add(request):
    if request.method != 'POST':
        form = Server_infoForm()
    else:
        form = Server_infoForm(request.POST)
        item_ip = request.POST.get('ip_address')
        if form.is_valid():
            form.save()
            messages.success(request, "数据%s添加成功！" % item_ip)
            return HttpResponseRedirect(reverse('servermanger:server_list'))
    content = {'form': form}
    return render(request, 'servermanger/add.html', content)

@login_required()
@permission_required('servermanger.delete_server_info', 'servermanger.add_server_info', 'servermanger.change_server_info')
def server_search(request):
    q = request.GET.get('keyword')
    if not q:
        pass

    pwd_list = Server_info.objects.filter(
        Q(position__icontains=q) | Q(server_type__icontains=q) | Q(sn__icontains=q) | Q(ip_address__icontains=q) | Q(
            host_name__icontains=q) | Q(user_name__icontains=q) | Q(password__icontains=q) | Q(mgmt_ip__icontains=q) | Q(
            mgmt_user__icontains=q) | Q(mgmt_pass__icontains=q) | Q(op__icontains=q) | Q(order__icontains=q) | Q(
            ma_info__icontains=q) | Q(apps__icontains=q)).order_by('-changed_time')
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
    return render(request, 'servermanger/list.html', content)

@login_required()
def api_update_phy(request):
    if request.method != 'POST':
        return HttpResponse("404")
    else:
        ip = request.POST.get('ip')
        password = request.POST.get('password')
        if Server_info.objects.filter(ip_address=ip).update(password=password):
            return HttpResponse("OK")
        else:
            return HttpResponse("ERROR")

def work_list(request):
    result={}
    if request.method=='POST':
        all_result=Server_info.objects.all().order_by('-changed_time')
        recordsTotal=all_result.count()
        recordsFiltered=recordsTotal

        start=int(request.POST['start'])
        length=int(request.POST['length'])
        draw=int(request.POST['draw'])
        new_search=request.POST['search[value]']
        new_order=request.POST['order[0][column]']
        by_name=request.POST['columns[{0}][data]'.format(new_order)]
        fun_order=request.POST['order[0][dir]']

        if by_name:
            if fun_order=="asc":
                all_result=all_result.order_by(by_name)
            else:
                all_result=all_result.order_by("-{0}".format(by_name))

        if new_search:
            all_result=all_result.filter(Q(position__icontains=new_search) | Q(server_type__icontains=new_search) | Q(sn__icontains=new_search) | Q(ip_address__icontains=new_search) | Q(
            host_name__icontains=new_search) | Q(user_name__icontains=new_search) | Q(password__icontains=new_search) | Q(mgmt_ip__icontains=new_search) | Q(
            mgmt_user__icontains=new_search) | Q(mgmt_pass__icontains=new_search) | Q(op__icontains=new_search) | Q(order__icontains=new_search) | Q(
            ma_info__icontains=new_search) | Q(apps__icontains=new_search))

        datas=all_result[start:(start+length)]
        resp=[obj.as_dict() for obj in datas]
        result={
            'draw':draw,
            'recordsTotal':recordsTotal,
            'recordsFiltered':recordsFiltered,
            'data':resp,
        }
        print(result)
        print(json.dumps(result))

    # return HttpResponse(json.dumps(result),content_type="application/json")
    return render(request, 'servermanger/list2.html', result)

def page_not_found(request):
    return render(request, 'servermanger/404.html')

#
# def page_error(request):
#     return render(request, '500.html')
#
#
# def permission_denied(request):
#     return render(request, '403.html')