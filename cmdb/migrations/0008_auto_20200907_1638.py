# Generated by Django 2.2.3 on 2020-09-07 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0007_auto_20200907_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='ops_admin',
            field=models.CharField(blank=True, help_text='运维全景图测试账号', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='ops_password',
            field=models.CharField(blank=True, help_text='运维全景图测试账号密码', max_length=100, null=True),
        ),
    ]
