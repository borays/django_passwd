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

    if request.method != 'POST':
        form = Server_infoForm(instance=entry)
    else:
        form = Server_infoForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('servermanger:server_list'))
    content = {'entry': entry, 'form': form}
    return render(request, 'servermanger/edit.html', content)

@login_required()
@permission_required('servermanger.delete_server_info', 'servermanger.add_server_info', 'servermanger.change_server_info')
def server_delete(request, item_id):
    Server_info.objects.get(id=item_id).delete()
    return HttpResponseRedirect(reverse('servermanger:server_list'))

@login_required()
@permission_required('servermanger.delete_server_info', 'servermanger.add_server_info', 'servermanger.change_server_info')
def server_add(request):
    if request.method != 'POST':
        form = Server_infoForm()
    else:
        form = Server_infoForm(request.POST)
        if form.is_valid():
            form.save()
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