# Generated by Django 2.0.7 on 2018-07-08 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pwdmanger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwd_info',
            name='changed_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]