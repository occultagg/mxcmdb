# Generated by Django 2.2.3 on 2020-09-09 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0015_auto_20200909_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='mac',
            field=models.CharField(blank=True, help_text='物理地址', max_length=50, null=True),
        ),
    ]
