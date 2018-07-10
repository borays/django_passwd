from django.db import models


# Create your models here.
class Passwd_info(models.Model):
    ip_address = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now_add=True)
    changed_time = models.DateTimeField(auto_now=True)
    os_type = models.CharField(max_length=200)

    def __str__(self):
        return self.ip_address
