from django.db import models

# Create your models here.
class Server_info(models.Model):
    position = models.CharField(max_length=200,unique=True,verbose_name="机柜位置")
    server_type = models.CharField(max_length=200,verbose_name="设备型号")
    created_time = models.DateTimeField(auto_now_add=True)
    changed_time = models.DateTimeField(auto_now=True)
    sn = models.CharField(max_length=200, verbose_name="序列号")
    ip_address = models.CharField(max_length=200,unique=True, verbose_name="IP地址")
    user_name=models.CharField(max_length=200,verbose_name="用户名")
    password = models.CharField(max_length=200, verbose_name="密码")
    mgmt_ip = models.CharField(max_length=200, verbose_name="管理IP")
    mgmt_user = models.CharField(max_length=200, verbose_name="管理用户名")
    mgmt_pass = models.CharField(max_length=200, verbose_name="管理密码")
    apps = models.CharField(max_length=200, verbose_name="项目名")
    order=models.CharField(max_length=200,blank=True,verbose_name="负责人")
    op=models.CharField(max_length=200,verbose_name="维护人")
    host_name = models.CharField(max_length=20, verbose_name="主机名", blank=True)
    ma_info = models.DateField(max_length=20, verbose_name="过保日期", blank=True)


    def __str__(self):
        return self.ip_address

    class Meta:
        get_latest_by ="changed_time"
        verbose_name = "物理机管理"