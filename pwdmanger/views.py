from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
# Create your views here.

from .models import Passwd_info
from .forms import Passwd_infoForm

#for limits
from django.contrib.auth.decorators import login_required,permission_required

@login_required()
def index(request):
    return render(request,'pwdmanger/index.html')

def test(request):
    return render(request,'pwdmanger/list.html')

@permission_required('pwdmanger.delete_passwd_info','pwdmanger.add_passwd_info','pwdmanger.change_passwd_info')
@login_required()
def passwd_list(request):
    pwd_list=Passwd_info.objects.all().order_by('changed_time')
    content={'pwd_list':pwd_list}
    return render(request,'pwdmanger/list.html',content)

@permission_required('pwdmanger.delete_passwd_info','pwdmanger.add_passwd_info','pwdmanger.change_passwd_info')
@login_required()
def passwd_edit(request,item_id):
    entry=Passwd_info.objects.get(id=item_id)

    if request.method!='POST':
        form=Passwd_infoForm(instance=entry)
    else:
        form=Passwd_infoForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pwdmanger:passwd_list'))
    content={'entry':entry,'form':form}
    return render(request,'pwdmanger/edit.html',content)

@permission_required('pwdmanger.delete_passwd_info','pwdmanger.add_passwd_info','pwdmanger.change_passwd_info')
@login_required()
def passwd_add(request):
    if request.method !='POST':
        form=Passwd_infoForm()
    else:
        form=Passwd_infoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pwdmanger:passwd_list'))
    content={'form':form}
    return render(request,'pwdmanger/add.html',content)

@permission_required('pwdmanger.delete_passwd_info','pwdmanger.add_passwd_info','pwdmanger.change_passwd_info')
@login_required()
def passwd_delete(request,item_id):
    Passwd_info.objects.get(id=item_id).delete()
    return HttpResponseRedirect(reverse('pwdmanger:passwd_list'))