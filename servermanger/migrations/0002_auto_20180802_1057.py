# Generated by Django 2.0.7 on 2018-08-02 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servermanger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server_info',
            name='ma_info',
            field=models.DateField(blank=True, max_length=20, verbose_name='过保日期'),
        ),
    ]
