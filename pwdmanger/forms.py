from django import forms

from .models import Passwd_info


class Passwd_infoForm(forms.ModelForm):
    class Meta:
        model = Passwd_info
        fields = ['ip_address', 'password', 'os_type', 'user_name', 'cluster_name', 'order', 'apps', 'host_name','op']
        labels = {'ip_address': 'IP地址', 'password': '密码', 'os_type': '系统', 'user_name': '用户名', 'cluster_name': '集群名',
                  'order': '负责人', 'apps': '应用', 'host_name': '主机名','op':'运维人'}
