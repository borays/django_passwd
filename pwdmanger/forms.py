from django import forms

from .models import Passwd_info

class Passwd_infoForm(forms.ModelForm):
    class Meta:
        model=Passwd_info
        fields = ['ip_address', 'password','os_type' ]
        labels = {'ip_address': 'IP地址', 'password': '密码','os_type':'系统'}