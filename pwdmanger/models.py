from django.db import models


# Create your models here.
class Passwd_info(models.Model):
    ip_address = models.CharField(max_length=200,unique=True,verbose_name="IP地址")
    password = models.CharField(max_length=200,verbose_name="密码")
    created_time = models.DateTimeField(auto_now_add=True)
    changed_time = models.DateTimeField(auto_now=True)
    os_type = models.CharField(max_length=200,verbose_name="系统类型")
    user_name=models.CharField(max_length=200,verbose_name="用户名")
    cluster_name=models.CharField(max_length=200,verbose_name="集群名")
    order=models.CharField(max_length=200,blank=True,verbose_name="负责人")
    apps=models.CharField(max_length=200,verbose_name="应用名")
    host_name=models.CharField(max_length=20,verbose_name="主机名",unique=True)
    op=models.CharField(max_length=200,verbose_name="维护人")

    def __str__(self):
        return self.ip_address

    class Meta:
        get_latest_by ="changed_time"
        verbose_name = "虚拟机密码表"
