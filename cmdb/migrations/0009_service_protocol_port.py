# Generated by Django 2.2.3 on 2020-09-08 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0008_auto_20200907_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='protocol_port',
            field=models.CharField(blank=True, help_text='请输入协议和端口,"-"连接,例如"TCP-8080",多个协议端口请用";"分割', max_length=100),
        ),
    ]
