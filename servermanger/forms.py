from django import forms
from .models import Server_info


class Server_infoForm(forms.ModelForm):
    class Meta:
        model = Server_info
        fields = ['position', 'server_type', 'sn', 'ip_address', 'user_name',
                  'password', 'mgmt_ip', 'mgmt_user', 'mgmt_pass', 'apps', 'order', 'op', 'host_name', 'ma_info']
        labels = {'position': '机架位置', 'server_type': '型号', 'sn': '序列号', 'ip_address': 'IP地址', 'user_name': '用户名',
                  'password': '密码', 'mgmt_ip': '管理IP', 'mgmt_user': '管理用户', 'mgmt_pass': '管理密码', 'apps': '应用',
                  'order': '负责人', 'op': '运维人', 'host_name': '主机名', 'ma_info': '维保信息'}
